import typer
from app import ingest, dashboard, onboard_user, init_db
from app.logging_config import configure_logging
from app.payments import PaymentService

app = typer.Typer(help="Cypher command line interface")

@app.command()
def run_ingestion(contracts: str, streaming: str):
    """Run the ingestion pipeline."""
    configure_logging()
    ingest.run_ingestion(contracts, streaming)

@app.command()
def run_payments():
    """Process unpaid revenue and manage streams."""
    configure_logging()
    PaymentService().process_unpaid_revenue()

@app.command()
def onboard_user(holder_id: int):
    """Verify a rights holder via simulated KYC."""
    configure_logging()
    onboard_user.onboard(holder_id)

@app.command()
def start_dashboard():
    """Start the Flask dashboard."""
    configure_logging()
    dashboard.app.run(debug=True)

if __name__ == "__main__":
    init_db()
    app()
