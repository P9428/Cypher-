"""Tests for the PaymentService business logic."""
from unittest import mock

from app import database, models
from app.payments import PaymentService


def setup_db(tmp_path):
    db_path = tmp_path / "test.db"
    engine = database.create_engine(f"sqlite:///{db_path}", echo=False, future=True)
    database.SessionLocal.configure(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return engine


def create_holder(session, verified=True, flow_rate=0):
    holder = models.RightsHolder(name="Alice", wallet="0x1", kyc_status="verified" if verified else "pending",
                                 superfluid_flow_rate=flow_rate)
    session.add(holder)
    session.commit()
    return holder


def create_token(session, holder):
    token = models.Token(track_id="track1", share=1.0, holder_id=holder.id)
    session.add(token)
    session.commit()
    return token


def create_stream(session, revenue=100.0):
    stream = models.StreamingData(track_id="track1", revenue=revenue, processed=False)
    session.add(stream)
    session.commit()
    return stream


def test_calculate_flow_rate(monkeypatch, tmp_path):
    setup_db(tmp_path)
    session = database.SessionLocal()
    holder = create_holder(session)
    create_token(session, holder)
    create_stream(session, 90.0)
    session.close()

    ps = PaymentService()
    mocked = mock.Mock()
    monkeypatch.setattr(ps, "_update_onchain_stream", mocked)

    ps.process_unpaid_revenue()

    assert mocked.call_count == 1
    args, _ = mocked.call_args
    # amount 90 -> flow rate calculation in _update_onchain_stream
    assert args[2] == 90.0


def test_skip_same_flow_rate(monkeypatch, tmp_path):
    setup_db(tmp_path)
    session = database.SessionLocal()
    holder = create_holder(session, flow_rate=100)
    create_token(session, holder)
    create_stream(session, 50.0)
    session.close()

    ps = PaymentService()
    # patch sf.create_or_update_flow to track calls
    monkeypatch.setattr(ps.sf, "create_or_update_flow", mock.Mock())

    # new flow rate computed inside _update_onchain_stream
    ps._update_onchain_stream(database.SessionLocal(), holder, 0.0)
    assert ps.sf.create_or_update_flow.call_count == 0


def test_skip_unverified_holder(monkeypatch, tmp_path):
    setup_db(tmp_path)
    session = database.SessionLocal()
    holder = create_holder(session, verified=False)
    create_token(session, holder)
    create_stream(session, 100.0)
    session.close()

    ps = PaymentService()
    mocked = mock.Mock()
    monkeypatch.setattr(ps.sf, "create_or_update_flow", mocked)

    ps.process_unpaid_revenue()
    assert mocked.call_count == 0


