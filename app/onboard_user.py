"""Simulated KYC onboarding script."""
import argparse
import logging

from .logging_config import configure_logging

from .database import SessionLocal
from .models import RightsHolder


def onboard(holder_id: int):
    """Mark a rights holder as verified in the database."""
    session = SessionLocal()
    holder = session.get(RightsHolder, holder_id)
    if not holder:
        session.close()
        raise ValueError(f"RightsHolder {holder_id} not found")
    holder.kyc_status = "verified"
    session.commit()
    session.close()
    logging.info(f"Holder {holder.name} verified")


if __name__ == '__main__':
    configure_logging()
    parser = argparse.ArgumentParser(description='Simulate KYC onboarding')
    parser.add_argument('holder_id', type=int)
    args = parser.parse_args()
    onboard(args.holder_id)
