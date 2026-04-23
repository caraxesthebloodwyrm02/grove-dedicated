"""Tests for temporal_safety: AsyncTemporalContext, TemporalPropertyGuard, signature_auth."""

from datetime import datetime
from zoneinfo import ZoneInfo

from grid.temporal_profile import OperationalMode, TimezoneProfile
from grid.temporal_safety import (
    AsyncTemporalContext,
    TemporalPropertyGuard,
    build_temporal_context,
    get_temporal_context,
    require_afterhours_signature,
    temporal_context_ctx,
    verify_push_signature,
)
from grid.temporal_safety.signature_auth import compute_push_signature


def test_build_temporal_context():
    """build_temporal_context produces valid AsyncTemporalContext."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=6, day_end_hour=22)
    now = datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
    ctx = build_temporal_context(profile=profile, now=now)
    assert ctx.profile == profile
    assert ctx.mode == OperationalMode.DAYTIME
    assert ctx.now == now
    assert ctx.time_window_id == "2025-03-02T10"


def test_context_var_propagation():
    """temporal_context_ctx propagates within async context."""
    ctx = build_temporal_context()
    token = temporal_context_ctx.set(ctx)
    try:
        assert get_temporal_context() is ctx
    finally:
        temporal_context_ctx.reset(token)
    assert get_temporal_context() is None


def test_temporal_property_guard_encrypt_decrypt_roundtrip():
    """TemporalPropertyGuard encrypt/decrypt round-trip preserves data."""
    profile = TimezoneProfile(timezone="UTC")
    now = datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=now,
        time_window_id="2025-03-02T10",
    )
    base_key = b"0" * 32
    guard = TemporalPropertyGuard(base_key=base_key)

    data = {
        "id": "x",
        "created_at": "2025-03-02T10:00:00Z",
        "expires_at": "2025-03-03T10:00:00Z",
    }
    encrypted = guard.encrypt(data, ctx)
    assert encrypted["created_at"] != data["created_at"]
    assert encrypted["expires_at"] != data["expires_at"]
    assert encrypted["id"] == "x"

    decrypted = guard.decrypt(encrypted, ctx)
    assert decrypted["created_at"] == data["created_at"]
    assert decrypted["expires_at"] == data["expires_at"]
    assert decrypted["id"] == "x"


def test_temporal_property_guard_ignores_non_sensitive():
    """TemporalPropertyGuard only touches marked fields."""
    profile = TimezoneProfile(timezone="UTC")
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    guard = TemporalPropertyGuard(base_key=b"0" * 32)
    data = {"other_field": "unchanged"}
    encrypted = guard.encrypt(data, ctx)
    assert encrypted["other_field"] == "unchanged"


def test_temporal_property_guard_preserves_none_sensitive_values():
    """Sensitive fields with None stay untouched instead of being serialized."""
    profile = TimezoneProfile(timezone="UTC")
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    guard = TemporalPropertyGuard(base_key=b"0" * 32)
    data = {"created_at": None, "mode_switch_time": None}

    encrypted = guard.encrypt(data, ctx)

    assert encrypted == data
    assert guard.decrypt(encrypted, ctx) == data


def test_temporal_property_guard_decrypt_fail_closed(monkeypatch):
    """Decrypt failures leave protected fields encrypted rather than corrupting values."""
    profile = TimezoneProfile(timezone="UTC")
    ctx = AsyncTemporalContext(
        profile=profile,
        mode=OperationalMode.DAYTIME,
        now=datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        time_window_id="2025-03-02T10",
    )
    guard = TemporalPropertyGuard(base_key=b"0" * 32)
    data = {"created_at": "2025-03-02T10:00:00Z"}
    encrypted = guard.encrypt(data, ctx)

    def fail_decrypt(*args, **kwargs):
        raise ValueError("bad ciphertext")

    monkeypatch.setattr(guard, "_decrypt_value", fail_decrypt)

    decrypted = guard.decrypt(encrypted, ctx)

    assert decrypted["created_at"] == encrypted["created_at"]
    assert decrypted["created_at"] != data["created_at"]


def test_verify_push_signature_valid():
    """verify_push_signature returns True for valid signature."""
    secret = b"shared_secret"
    body = b'{"data":"test"}'
    timestamp = "2025-03-02T10:00:00Z"
    sig = compute_push_signature(body, timestamp, OperationalMode.AFTERHOURS, secret)
    assert verify_push_signature(
        body=body,
        timestamp=timestamp,
        signature=sig,
        mode=OperationalMode.AFTERHOURS,
        secret=secret,
    )


def test_verify_push_signature_invalid():
    """verify_push_signature returns False for tampered body."""
    secret = b"shared_secret"
    body = b'{"data":"test"}'
    timestamp = "2025-03-02T10:00:00Z"
    sig = compute_push_signature(body, timestamp, OperationalMode.AFTERHOURS, secret)
    assert not verify_push_signature(
        body=b'{"data":"tampered"}',
        timestamp=timestamp,
        signature=sig,
        mode=OperationalMode.AFTERHOURS,
        secret=secret,
    )


def test_require_afterhours_signature_valid():
    """require_afterhours_signature accepts a valid afterhours signature."""
    secret = b"shared_secret"
    body = b'{"data":"test"}'
    timestamp = "2025-03-02T23:00:00Z"
    sig = compute_push_signature(body, timestamp, OperationalMode.AFTERHOURS, secret)

    assert require_afterhours_signature(body, timestamp, sig, secret)


def test_require_afterhours_signature_missing_headers():
    """require_afterhours_signature fails closed when auth headers are missing."""
    secret = b"shared_secret"
    body = b'{"data":"test"}'

    assert not require_afterhours_signature(body, None, "abc", secret)
    assert not require_afterhours_signature(body, "2025-03-02T23:00:00Z", None, secret)
