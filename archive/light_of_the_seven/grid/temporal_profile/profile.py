"""Geographic time-based profile and operational mode resolution."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OperationalMode(str, Enum):
    """Operational mode driven by geographic time."""

    DAYTIME = "daytime"
    AFTERHOURS = "afterhours"


class TimezoneProfile(BaseModel):
    """Profile for geographic time sync with single timezone source."""

    timezone: str = Field(default="UTC", description="IANA timezone string (e.g. America/New_York)")
    day_start_hour: int = Field(
        default=6, ge=0, le=23, description="Hour (local) when daytime begins"
    )
    day_end_hour: int = Field(default=22, ge=0, le=23, description="Hour (local) when daytime ends")


def resolve_operational_mode(
    profile: TimezoneProfile, now: Optional[datetime] = None
) -> OperationalMode:
    """Resolve operational mode from profile and current local time.

    Args:
        profile: Timezone profile with timezone and day window
        now: Optional datetime (UTC). Defaults to now if not provided.

    Returns:
        DAYTIME if local hour in [day_start_hour, day_end_hour), else AFTERHOURS
    """
    import zoneinfo

    if now is None:
        now = datetime.now(zoneinfo.ZoneInfo("UTC"))

    try:
        tz = zoneinfo.ZoneInfo(profile.timezone)
    except zoneinfo.ZoneInfoNotFoundError:
        tz = zoneinfo.ZoneInfo("UTC")

    local = now.astimezone(tz)
    hour = local.hour

    if profile.day_start_hour <= profile.day_end_hour:
        in_day = profile.day_start_hour <= hour < profile.day_end_hour
    else:
        # Spanning midnight (e.g. 22-6)
        in_day = hour >= profile.day_start_hour or hour < profile.day_end_hour

    return OperationalMode.DAYTIME if in_day else OperationalMode.AFTERHOURS


def get_default_profile() -> TimezoneProfile:
    """Get default profile from TZ env or config."""
    import os

    def read_hour(name: str, default: int) -> int:
        raw_value = os.environ.get(name)
        if raw_value is None:
            return default

        try:
            parsed = int(raw_value)
        except ValueError:
            return default

        if 0 <= parsed <= 23:
            return parsed
        return default

    tz = os.environ.get("TZ", "UTC")
    day_start = read_hour("TEMPORAL_DAY_START", 6)
    day_end = read_hour("TEMPORAL_DAY_END", 22)
    return TimezoneProfile(timezone=tz, day_start_hour=day_start, day_end_hour=day_end)
