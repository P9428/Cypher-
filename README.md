# Cypher Framework

Cypher is a prototype royalty distribution platform built on the Base Goerli testnet. It demonstrates how music streaming revenue can be ingested, tokenized and streamed to rights holders in real time using the Superfluid protocol.

## Project Goals
- Provide an end-to-end example of royalty ingestion, compliance checks and on-chain payouts.
- Showcase a "glass box" dashboard where rights holders can verify their earnings and transaction history.
- Serve as a lightweight framework for experimenting with blockchain‑based royalty flows.

## Architecture Overview
```
CSV Contracts & Revenue
        ↓
Ingestion Service
        ↓
SQLite Database
        ↓
Payment Service (Superfluid SDK)
        ↓
Base Goerli Network
        ↓
Flask Dashboard
```
The project uses a simple SQLite database for demo purposes. Each rights holder is onboarded with simulated KYC and their wallet is screened via Chainalysis before a payment stream is created.

## Repository Layout
- `app/` – application modules
  - `ingest.py` – load contract and streaming CSV data into the database
  - `onboard_user.py` – mark a rights holder as KYC verified
  - `payments.py` – calculate revenue and manage Superfluid streams
  - `dashboard.py` – Flask web server presenting the glass box dashboard
  - `config.py` – configuration values loaded from environment variables
  - `database.py`, `models.py` – SQLAlchemy setup and schema
  - `logging_config.py` – JSON logging setup
- `data/` – example contract and streaming CSVs
- `tests/` – unit tests for ingestion and payment logic
- `main.py` – Typer CLI entry point

## Setup and Installation
1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd Cypher-
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
4. **Configure environment variables**
   - Copy `.env.example` to `.env` and provide values for:
     - `TREASURY_WALLET_PRIVATE_KEY` – private key for the treasury wallet
     - `BASE_GOERLI_RPC_URL` – RPC endpoint for Base Goerli
     - `USDCX_ADDRESS` – USDCx Super Token contract address
     - `CHAINALYSIS_API_KEY` and `CHAINALYSIS_API_URL` – wallet screening API
     - `DISTRIBUTION_PERIOD_SECONDS` – payout period (default 30 days)
     - `CHAINALYSIS_RISK_THRESHOLD` – maximum allowed risk score
5. **Initialize the database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

## Usage Workflow
1. **Run ingestion**
   ```bash
   python main.py run-ingestion --contracts data/contracts.csv --streaming data/streaming.csv
   ```
2. **Onboard a rights holder**
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
   Visit `http://127.0.0.1:5000` to view the real-time dashboard.

## Running Tests
To run the unit tests:
```bash
pytest -q
```

The tests cover data ingestion and the PaymentService business logic. You may need the project dependencies installed beforehand.
