"""Tests for temporal_profile: TimezoneProfile, OperationalMode, resolve_operational_mode."""

from datetime import datetime
from zoneinfo import ZoneInfo

from grid.temporal_profile import (
    OperationalMode,
    TimezoneProfile,
    get_default_profile,
    resolve_operational_mode,
)


def test_resolve_operational_mode_daytime():
    """Daytime: hour in [6, 22) returns DAYTIME."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=6, day_end_hour=22)
    # 10:00 UTC
    now = datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.DAYTIME


def test_resolve_operational_mode_afterhours():
    """Afterhours: hour outside [6, 22) returns AFTERHOURS."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=6, day_end_hour=22)
    # 23:00 UTC
    now = datetime(2025, 3, 2, 23, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.AFTERHOURS


def test_resolve_operational_mode_boundary_start():
    """Boundary: hour 6 is daytime (inclusive start)."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=6, day_end_hour=22)
    now = datetime(2025, 3, 2, 6, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.DAYTIME


def test_resolve_operational_mode_boundary_end():
    """Boundary: hour 22 is afterhours (exclusive end)."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=6, day_end_hour=22)
    now = datetime(2025, 3, 2, 22, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.AFTERHOURS


def test_resolve_operational_mode_overnight_boundary_start():
    """Overnight windows treat the start hour as inclusive daytime."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=22, day_end_hour=6)
    now = datetime(2025, 3, 2, 22, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.DAYTIME


def test_resolve_operational_mode_overnight_boundary_end():
    """Overnight windows treat the end hour as exclusive daytime."""
    profile = TimezoneProfile(timezone="UTC", day_start_hour=22, day_end_hour=6)
    now = datetime(2025, 3, 3, 6, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.AFTERHOURS


def test_resolve_operational_mode_america_new_york():
    """Profile uses timezone for local hour."""
    profile = TimezoneProfile(timezone="America/New_York", day_start_hour=6, day_end_hour=22)
    # 02:00 UTC = 21:00 EST (daytime in Eastern)
    now = datetime(2025, 3, 2, 2, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.DAYTIME


def test_resolve_operational_mode_invalid_timezone_falls_back_to_utc():
    """Unknown timezones fall back to UTC instead of raising."""
    profile = TimezoneProfile(timezone="Mars/Phobos", day_start_hour=6, day_end_hour=22)
    now = datetime(2025, 3, 2, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert resolve_operational_mode(profile, now) == OperationalMode.DAYTIME


def test_get_default_profile_from_env(monkeypatch):
    """get_default_profile reads TZ from environment."""
    monkeypatch.setenv("TZ", "America/Los_Angeles")
    monkeypatch.setenv("TEMPORAL_DAY_START", "8")
    monkeypatch.setenv("TEMPORAL_DAY_END", "20")
    profile = get_default_profile()
    assert profile.timezone == "America/Los_Angeles"
    assert profile.day_start_hour == 8
    assert profile.day_end_hour == 20


def test_get_default_profile_fallback(monkeypatch):
    """get_default_profile uses UTC when TZ unset."""
    monkeypatch.delenv("TZ", raising=False)
    profile = get_default_profile()
    assert profile.timezone == "UTC"


def test_get_default_profile_invalid_hours_fall_back_to_defaults(monkeypatch):
    """Malformed or out-of-range env hours do not break default profile creation."""
    monkeypatch.setenv("TEMPORAL_DAY_START", "not-an-int")
    monkeypatch.setenv("TEMPORAL_DAY_END", "24")
    profile = get_default_profile()
    assert profile.day_start_hour == 6
    assert profile.day_end_hour == 22
