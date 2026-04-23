"""Async temporal context with contextvars propagation."""

from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from grid.temporal_profile import OperationalMode, TimezoneProfile, resolve_operational_mode

temporal_context_ctx: ContextVar[Optional["AsyncTemporalContext"]] = ContextVar(
    "temporal_context", default=None
)


class AsyncTemporalContext(BaseModel):
    """Temporal context bound to async flow: profile, mode, now, time_window_id."""

    profile: TimezoneProfile = Field(description="Timezone profile")
    mode: OperationalMode = Field(description="Current operational mode")
    now: datetime = Field(description="Timezone-aware current time")
    time_window_id: str = Field(
        description="Time window ID for key derivation (e.g. 2025-03-02T09)"
    )

    class Config:
        arbitrary_types_allowed = True


def get_temporal_context() -> Optional[AsyncTemporalContext]:
    """Get current AsyncTemporalContext from contextvars."""
    return temporal_context_ctx.get()


def build_temporal_context(
    profile: Optional[TimezoneProfile] = None,
    now: Optional[datetime] = None,
) -> AsyncTemporalContext:
    """Build AsyncTemporalContext from profile and optional now."""
    from grid.temporal_profile import get_default_profile

    if profile is None:
        profile = get_default_profile()

    if now is None:
        import zoneinfo

        now = datetime.now(zoneinfo.ZoneInfo("UTC"))

    mode = resolve_operational_mode(profile, now)
    time_window_id = now.strftime("%Y-%m-%dT%H")

    return AsyncTemporalContext(
        profile=profile,
        mode=mode,
        now=now,
        time_window_id=time_window_id,
    )
