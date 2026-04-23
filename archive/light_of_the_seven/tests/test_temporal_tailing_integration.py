"""Integration tests: temporal safety + tailing + middleware + PeriodicProcessor."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from application.mothership.middleware import TemporalContextMiddleware
from grid.processing.periodic_processor import PeriodicProcessor, ProcessingSchedule
from grid.tailing import ChainExecutor, OnCompletion, OnCondition, TailingChain
from grid.temporal_profile import OperationalMode, TimezoneProfile
from grid.temporal_safety import (
    AsyncTemporalContext,
    TemporalPropertyGuard,
    get_temporal_context,
    temporal_context_ctx,
)


@pytest.fixture
def app_with_temporal_middleware():
    """FastAPI app with TemporalContextMiddleware only (minimal for integration)."""
    app = FastAPI()

    @app.get("/temporal")
    async def get_temporal():
        ctx = get_temporal_context()
        if ctx is None:
            return {"mode": None, "time_window_id": None}
        return {"mode": ctx.mode.value, "time_window_id": ctx.time_window_id}

    app.add_middleware(TemporalContextMiddleware)
    return app


def test_temporal_context_middleware_sets_context(app_with_temporal_middleware):
    """TemporalContextMiddleware sets AsyncTemporalContext for request scope."""
    with TestClient(app_with_temporal_middleware) as client:
        r = client.get("/temporal")
    assert r.status_code == 200
    data = r.json()
    assert "mode" in data
    assert "time_window_id" in data
    assert data["mode"] in ("daytime", "afterhours")
    assert data["time_window_id"] is not None


@pytest.mark.asyncio
async def test_tailing_chain_with_temporal_property_guard():
    """Integration: tailing chain validate -> encrypt using TemporalPropertyGuard."""
    profile = TimezoneProfile(timezone="UTC")
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    token = temporal_context_ctx.set(ctx)
    try:
        guard = TemporalPropertyGuard(base_key=b"0" * 32)

        def validate(x):
            assert "created_at" in x
            return x

        def encrypt_step(x):
            return guard.encrypt(x, get_temporal_context())

        chain = TailingChain()
        chain.append(validate, OnCompletion())
        chain.append(encrypt_step, OnCondition(lambda d: "created_at" in d))

        executor = ChainExecutor(chain)
        data = {"id": "a", "created_at": "2025-03-02T10:00:00Z"}
        result = await executor.run(data)
        assert result["id"] == "a"
        assert result["created_at"] != data["created_at"]
    finally:
        temporal_context_ctx.reset(token)


@pytest.mark.asyncio
async def test_periodic_processor_sets_temporal_context():
    """PeriodicProcessor sets AsyncTemporalContext during _process_cycle."""
    captured = []

    def processor(batch):
        ctx = get_temporal_context()
        captured.append(ctx)
        return len(batch)

    proc = PeriodicProcessor(ProcessingSchedule(interval_seconds=999, batch_size=10))
    proc.set_processor(processor)
    proc.enqueue({"x": 1})

    await proc._process_cycle()

    assert len(captured) == 1
    assert captured[0] is not None
    assert isinstance(captured[0], AsyncTemporalContext)
    assert captured[0].mode in (OperationalMode.DAYTIME, OperationalMode.AFTERHOURS)
    assert captured[0].time_window_id is not None
