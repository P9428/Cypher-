"""Configuration loaded from environment variables."""
import os

TREASURY_WALLET_PRIVATE_KEY = os.getenv('TREASURY_WALLET_PRIVATE_KEY')
BASE_GOERLI_RPC_URL = os.getenv('BASE_GOERLI_RPC_URL')
USDCX_ADDRESS = os.getenv('USDCX_ADDRESS')
CHAINALYSIS_API_KEY = os.getenv('CHAINALYSIS_API_KEY')
CHAINALYSIS_API_URL = os.getenv('CHAINALYSIS_API_URL')

# Distribution period for revenue in seconds (default 30 days)
DISTRIBUTION_PERIOD_SECONDS = int(os.getenv('DISTRIBUTION_PERIOD_SECONDS', str(30 * 24 * 3600)))

# Risk threshold for Chainalysis wallet screening
CHAINALYSIS_RISK_THRESHOLD = int(os.getenv('CHAINALYSIS_RISK_THRESHOLD', '8'))
