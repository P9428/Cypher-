# Cypher Demo

Cypher is a blockchain-based royalty payment platform that uses Superfluid streaming to deliver real-time USDC earnings to rights holders. This repository contains a simplified prototype demonstrating the end-to-end flow from data ingestion to on-chain payments and a web dashboard.

## Architecture Overview
```
CSV files -> Ingestion Service -> SQLite DB -> Payment Service -> Base Goerli -> Flask Dashboard
```

## Setup and Installation
1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd Cypher
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment variables**
   - Copy `.env.example` to `.env` and fill in the required values:
     - `TREASURY_WALLET_PRIVATE_KEY` – private key for the treasury wallet
     - `BASE_GOERLI_RPC_URL` – RPC endpoint for Base Goerli
     - `USDCX_ADDRESS` – address of the USDCx Super Token contract
     - `CHAINALYSIS_API_KEY` – Chainalysis API key
     - `CHAINALYSIS_API_URL` – Chainalysis KYT endpoint
     - `DISTRIBUTION_PERIOD_SECONDS` – period for revenue distribution (default 30 days)
     - `CHAINALYSIS_RISK_THRESHOLD` – max acceptable wallet risk score

5. **Initialize the database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

## Usage Workflow
1. **Run ingestion**
   ```bash
   python main.py run-ingestion --contracts data/contracts.csv --streaming data/streaming.csv
   ```
2. **Onboard a rights holder** (simulated KYC)
   ```bash
   python main.py onboard-user --holder-id 1
   ```
3. **Process payments**
   ```bash
   python main.py run-payments
   ```
4. **Start the dashboard**
   ```bash
   python main.py start-dashboard
   ```

## Running Tests
Execute the test suite with:
```bash
pytest -q
```
