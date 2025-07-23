from app import database, ingest, models
from sqlalchemy import select


def test_ingest(tmp_path):
    db_path = tmp_path / 'test.db'
    engine = database.create_engine(f'sqlite:///{db_path}', echo=False, future=True)
    database.SessionLocal.configure(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    contracts = tmp_path / 'contracts.csv'
    contracts.write_text('name,wallet,track_id,share\nAlice,0x1,track1,1.0\n')
    streaming = tmp_path / 'streaming.csv'
    streaming.write_text('track_id,revenue\ntrack1,100\n')

    ingest.run_ingestion(str(contracts), str(streaming))
    session = database.SessionLocal()
    holders = session.execute(select(models.RightsHolder)).scalars().all()
    streams = session.execute(select(models.StreamingData)).scalars().all()
    session.close()
    assert len(holders) == 1
    assert len(streams) == 1
    assert streams[0].processed is False
    assert holders[0].kyc_status == 'pending'
