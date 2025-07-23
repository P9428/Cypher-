"""Payment orchestration using Superfluid on Base Goerli."""
import logging
from collections import defaultdict
from sqlalchemy import select
from web3 import Web3
from web3.exceptions import TransactionNotFound
from superfluid_sdk_py import Framework
import requests

from .database import SessionLocal
from .models import RightsHolder, Token, StreamingData
from .config import (
    TREASURY_WALLET_PRIVATE_KEY,
    BASE_GOERLI_RPC_URL,
    USDCX_ADDRESS,
    CHAINALYSIS_API_KEY,
    CHAINALYSIS_API_URL,
    DISTRIBUTION_PERIOD_SECONDS,
    CHAINALYSIS_RISK_THRESHOLD,
)
from .logging_config import configure_logging


class PaymentService:
    """Service for processing unpaid revenue and managing streams."""

    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(BASE_GOERLI_RPC_URL))
        self.sf = Framework(web3=self.w3, private_key=TREASURY_WALLET_PRIVATE_KEY)

    def process_unpaid_revenue(self) -> None:
        """Main entry point to process unprocessed streaming data."""
        session = SessionLocal()
        streams = (
            session.execute(select(StreamingData).where(StreamingData.processed.is_(False)))
            .scalars()
            .all()
        )
        tokens = session.execute(select(Token)).scalars().all()
        holders = {h.id: h for h in session.execute(select(RightsHolder)).scalars()}

        payments = self._calculate_payments(streams, tokens)

        for s in streams:
            s.processed = True

        for holder_id, amount in payments.items():
            holder = holders[holder_id]
            self._update_onchain_stream(session, holder, amount)

        session.commit()
        session.close()

    def _calculate_payments(self, streams, tokens):
        """Aggregate revenue per rights holder for unprocessed streams."""
        payments = defaultdict(float)
        for s in streams:
            share_total = sum(t.share for t in tokens if t.track_id == s.track_id)
            if not share_total:
                continue
            for t in [t for t in tokens if t.track_id == s.track_id]:
                payments[t.holder_id] += s.revenue * (t.share / share_total)
        return payments

    def _update_onchain_stream(self, session, holder: RightsHolder, amount: float) -> None:
        """Create or update a Superfluid stream for a rights holder."""
        logger = logging.getLogger(__name__)
        if holder.kyc_status != "verified":
            logger.warning(f"Skipping {holder.name}: KYC not verified")
            return

        risk = screen_wallet(holder.wallet)
        if risk >= CHAINALYSIS_RISK_THRESHOLD:
            logger.critical(
                f"High risk wallet for {holder.name}. Payment blocked.")
            return

        flow_rate = int((amount * (10 ** 18)) / DISTRIBUTION_PERIOD_SECONDS)

        if flow_rate == holder.superfluid_flow_rate:
            logger.info(f"No update needed for {holder.name}")
            return

        try:
            tx = self.sf.create_or_update_flow(
                sender=self.sf.wallet.address,
                receiver=holder.wallet,
                super_token=USDCX_ADDRESS,
                flow_rate=flow_rate,
            )
            receipt = self.w3.eth.wait_for_transaction_receipt(tx)
            holder.superfluid_stream_is_active = True
            holder.superfluid_flow_rate = flow_rate
            holder.last_updated_tx_hash = receipt.transactionHash.hex()
            logger.info(f"Successfully updated stream for holder_id: {holder.id}")
        except (TransactionNotFound, ValueError, requests.exceptions.RequestException) as e:
            holder.superfluid_stream_is_active = False
            logger.error(f"Failed to update stream for {holder.name}: {e}")


def screen_wallet(address: str) -> int:
    """Return Chainalysis risk score for a wallet or 0 if unavailable."""
    logger = logging.getLogger(__name__)
    if not CHAINALYSIS_API_KEY or not CHAINALYSIS_API_URL:
        return 0
    try:
        resp = requests.post(
            CHAINALYSIS_API_URL,
            json={"address": address},
            headers={"X-API-Key": CHAINALYSIS_API_KEY},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("risk", 0))
    except requests.RequestException as e:
        logger.error(f"Chainalysis API failure for {address}: {e}")
        return 0


if __name__ == "__main__":
    configure_logging()
    PaymentService().process_unpaid_revenue()
