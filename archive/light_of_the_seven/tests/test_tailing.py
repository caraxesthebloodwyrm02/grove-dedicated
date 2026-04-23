"""Tests for tailing: TailingChain, TailingTrigger, ChainExecutor."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from grid.tailing import (
    ChainExecutor,
    OnCompletion,
    OnCondition,
    OnModeChange,
    TailingChain,
)
from grid.temporal_profile import OperationalMode, TimezoneProfile
from grid.temporal_safety.context import AsyncTemporalContext, temporal_context_ctx


@pytest.fixture
def sample_chain():
    """Chain that doubles then adds 1."""

    def step1(x):
        return x * 2

    def step2(x):
        return x + 1

    chain = TailingChain()
    chain.append(step1, OnCompletion())
    chain.append(step2, OnCompletion())
    return chain


@pytest.mark.asyncio
async def test_chain_executor_on_completion(sample_chain):
    """ChainExecutor runs all steps with OnCompletion triggers."""
    executor = ChainExecutor(sample_chain)
    result = await executor.run(5)
    assert result == 11  # 5*2=10, 10+1=11


@pytest.mark.asyncio
async def test_chain_executor_stops_on_condition_false():
    """ChainExecutor stops when OnCondition predicate is False."""

    def step1(x):
        return {"value": x * 2, "status": "pending"}

    def step2(x):
        return {"value": x["value"] + 1, "status": "done"}

    chain = TailingChain()
    chain.append(step1, OnCompletion())
    chain.append(step2, OnCondition(lambda out: out.get("status") == "done"))

    executor = ChainExecutor(chain)
    result = await executor.run(5)
    assert result["status"] == "pending"
    assert result["value"] == 10
    assert "done" not in str(result)


@pytest.mark.asyncio
async def test_chain_executor_continues_on_condition_true():
    """ChainExecutor continues when OnCondition predicate is True."""

    def step1(x):
        return {"value": x, "ok": True}

    def step2(x):
        return x["value"] + 1

    chain = TailingChain()
    chain.append(step1, OnCompletion())
    chain.append(step2, OnCondition(lambda out: out.get("ok") is True))

    executor = ChainExecutor(chain)
    result = await executor.run(3)
    assert result == 4


@pytest.mark.asyncio
async def test_chain_executor_empty_chain():
    """Empty chain returns initial input."""
    chain = TailingChain()
    executor = ChainExecutor(chain)
    result = await executor.run(42)
    assert result == 42


@pytest.mark.asyncio
async def test_chain_executor_async_step():
    """ChainExecutor supports async steps."""

    async def async_step(x):
        return x + 10

    chain = TailingChain()
    chain.append(async_step, OnCompletion())
    executor = ChainExecutor(chain)
    result = await executor.run(1)
    assert result == 11


@pytest.mark.asyncio
async def test_chain_executor_single_step():
    """Single-step chain runs one step."""
    chain = TailingChain()
    chain.append(lambda x: x * 3, OnCompletion())
    executor = ChainExecutor(chain)
    result = await executor.run(7)
    assert result == 21


@pytest.mark.asyncio
async def test_tailing_chain_with_temporal_context():
    """Temporal context is available during chain execution (same async context)."""
    profile = TimezoneProfile(timezone="UTC")
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    token = temporal_context_ctx.set(ctx)
    try:

        def check_context(x):
            from grid.temporal_safety.context import get_temporal_context

            c = get_temporal_context()
            assert c is not None
            assert c.mode == OperationalMode.DAYTIME
            return x + 1

        chain = TailingChain()
        chain.append(check_context, OnCompletion())
        executor = ChainExecutor(chain)
        result = await executor.run(0)
        assert result == 1
    finally:
        temporal_context_ctx.reset(token)


# --- Trigger unit tests ---


def test_on_completion_should_fire_always():
    """OnCompletion.should_fire returns True regardless of output or error."""
    t = OnCompletion()
    assert t.should_fire(None, None) is True
    assert t.should_fire({"ok": True}, None) is True
    assert t.should_fire(None, ValueError("err")) is True


def test_on_condition_should_fire_when_predicate_true():
    """OnCondition.should_fire returns True when predicate(prior_output) is True."""
    t = OnCondition(lambda x: x > 5)
    assert t.should_fire(10, None) is True
    assert t.should_fire(6, None) is True


def test_on_condition_should_fire_false_when_predicate_false():
    """OnCondition.should_fire returns False when predicate(prior_output) is False."""
    t = OnCondition(lambda x: x > 5)
    assert t.should_fire(3, None) is False
    assert t.should_fire(5, None) is False


def test_on_condition_should_fire_false_when_prior_error():
    """OnCondition.should_fire returns False when prior_error is set."""
    t = OnCondition(lambda x: True)
    assert t.should_fire(99, RuntimeError("fail")) is False


def test_on_mode_change_should_fire_false_when_no_context():
    """OnModeChange.should_fire returns False when no temporal context."""
    t = OnModeChange(initial_mode=OperationalMode.DAYTIME)
    token = temporal_context_ctx.set(None)
    try:
        assert t.should_fire(1, None) is False
    finally:
        temporal_context_ctx.reset(token)


def test_on_mode_change_should_fire_false_when_mode_unchanged():
    """OnModeChange.should_fire returns False when mode equals initial_mode."""
    t = OnModeChange(initial_mode=OperationalMode.DAYTIME)
    ctx = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    token = temporal_context_ctx.set(ctx)
    try:
        assert t.should_fire(1, None) is False
    finally:
        temporal_context_ctx.reset(token)


def test_on_mode_change_should_fire_true_when_mode_changed():
    """OnModeChange.should_fire returns True when mode differs from initial_mode."""
    t = OnModeChange(initial_mode=OperationalMode.DAYTIME)
    ctx = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.AFTERHOURS,
        now=datetime(2025, 3, 2, 23, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T23",
    )
    token = temporal_context_ctx.set(ctx)
    try:
        assert t.should_fire(1, None) is True
    finally:
        temporal_context_ctx.reset(token)


def test_on_mode_change_should_fire_false_when_prior_error():
    """OnModeChange.should_fire returns False when prior_error is set."""
    t = OnModeChange(initial_mode=OperationalMode.DAYTIME)
    ctx = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.AFTERHOURS,
        now=datetime(2025, 3, 2, 23, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T23",
    )
    token = temporal_context_ctx.set(ctx)
    try:
        assert t.should_fire(1, ValueError("err")) is False
    finally:
        temporal_context_ctx.reset(token)


# --- OnModeChange chain tests ---


@pytest.mark.asyncio
async def test_chain_on_mode_change_no_context_step_skipped():
    """OnModeChange step is skipped when no temporal context."""

    def step1(x):
        return x + 1

    def step2(x):
        return x * 2

    chain = TailingChain()
    chain.append(step1, OnCompletion())
    chain.append(step2, OnModeChange())

    temporal_context_ctx.set(None)
    executor = ChainExecutor(chain)
    result = await executor.run(5)
    assert result == 6
    temporal_context_ctx.set(None)


@pytest.mark.asyncio
async def test_chain_on_mode_change_mode_unchanged_step_skipped():
    """OnModeChange step is skipped when mode has not changed."""
    ctx = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    token = temporal_context_ctx.set(ctx)
    try:

        def step1(x):
            return x + 1

        def step2(x):
            return x * 2

        chain = TailingChain()
        chain.append(step1, OnCompletion())
        chain.append(step2, OnModeChange())

        executor = ChainExecutor(chain)
        result = await executor.run(5)
        assert result == 6
    finally:
        temporal_context_ctx.reset(token)


@pytest.mark.asyncio
async def test_chain_on_mode_change_mode_changed_step_runs():
    """OnModeChange step runs when mode has changed from chain start."""
    ctx_daytime = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    ctx_afterhours = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.AFTERHOURS,
        now=datetime(2025, 3, 2, 23, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T23",
    )
    token = temporal_context_ctx.set(ctx_daytime)
    try:

        def step1(x):
            temporal_context_ctx.set(ctx_afterhours)
            return x + 1

        def step2(x):
            return x * 2

        chain = TailingChain()
        chain.append(step1, OnCompletion())
        chain.append(step2, OnModeChange())

        executor = ChainExecutor(chain)
        result = await executor.run(5)
        assert result == 12
    finally:
        temporal_context_ctx.reset(token)


@pytest.mark.asyncio
async def test_chain_multiple_on_mode_change_all_initialized():
    """Multiple OnModeChange triggers all get initial_mode set (no break bug)."""
    ctx = AsyncTemporalContext(
        profile=TimezoneProfile(timezone="UTC"),
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    token = temporal_context_ctx.set(ctx)
    try:

        def step1(x):
            return x + 1

        def step2(x):
            return x + 10

        def step3(x):
            return x + 100

        chain = TailingChain()
        chain.append(step1, OnCompletion())
        chain.append(step2, OnModeChange())
        chain.append(step3, OnModeChange())

        executor = ChainExecutor(chain)
        result = await executor.run(0)
        assert result == 1
    finally:
        temporal_context_ctx.reset(token)
