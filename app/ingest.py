"""Ingestion pipeline for royalty contracts and streaming data."""
from pathlib import Path
import pandas as pd
from .database import SessionLocal
from .models import RightsHolder, Token, StreamingData


def ingest_contracts(csv_path: Path, session):
    """Parse a royalty contract CSV and store rights holders and tokens."""
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        holder = RightsHolder(name=row["name"], wallet=row["wallet"])
        session.add(holder)
        session.flush()
        token = Token(
            track_id=row["track_id"],
            share=row["share"],
            holder_id=holder.id,
        )
        session.add(token)
    session.commit()


def ingest_streaming(csv_path: Path, session):
    """Load streaming revenue CSV data into the database."""
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        stream = StreamingData(
            track_id=row["track_id"],
            revenue=row["revenue"],
            processed=False,
        )
        session.add(stream)
    session.commit()


def run_ingestion(contract_csv: str, streaming_csv: str):
    """Run full ingestion of contracts and streaming data."""
    session = SessionLocal()
    ingest_contracts(Path(contract_csv), session)
    ingest_streaming(Path(streaming_csv), session)
    session.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run ingestion pipeline.')
    parser.add_argument('--contracts', required=True)
    parser.add_argument('--streaming', required=True)
    args = parser.parse_args()
    run_ingestion(args.contracts, args.streaming)
