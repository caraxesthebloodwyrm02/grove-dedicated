"""HMAC-SHA256 signature verification for afterhours data push."""

from __future__ import annotations

import hashlib
import hmac
from typing import Optional

from grid.temporal_profile import OperationalMode


def compute_push_signature(
    body: bytes,
    timestamp: str,
    mode: OperationalMode,
    secret: bytes,
) -> str:
    """Compute HMAC-SHA256 signature for data push.

    Args:
        body: Raw request body
        timestamp: X-Timestamp header value
        mode: Operational mode (AFTERHOURS)
        secret: Shared secret for HMAC

    Returns:
        Hex-encoded signature
    """
    material = body + timestamp.encode() + mode.value.encode()
    sig = hmac.new(secret, material, hashlib.sha256).hexdigest()
    return sig


def verify_push_signature(
    body: bytes,
    timestamp: str,
    signature: str,
    mode: OperationalMode,
    secret: bytes,
) -> bool:
    """Verify HMAC-SHA256 signature for afterhours data push.

    In afterhours mode, data push requests must include X-Signature and X-Timestamp.
    Signature is computed over (body + timestamp + mode).

    Args:
        body: Raw request body
        timestamp: X-Timestamp header value
        signature: X-Signature header value (hex-encoded)
        mode: Operational mode (must be AFTERHOURS for strict verification)
        secret: Shared secret for HMAC

    Returns:
        True if signature is valid
    """
    if not timestamp or not signature:
        return False
    expected = compute_push_signature(body, timestamp, mode, secret)
    return hmac.compare_digest(expected, signature)


def require_afterhours_signature(
    body: bytes,
    timestamp: Optional[str],
    signature: Optional[str],
    secret: bytes,
) -> bool:
    """Require valid signature when in afterhours mode.

    Convenience wrapper: returns True only if signature and timestamp are
    present and verify_push_signature succeeds with AFTERHOURS mode.
    """
    if timestamp is None or signature is None:
        return False
    return verify_push_signature(
        body=body,
        timestamp=timestamp,
        signature=signature,
        mode=OperationalMode.AFTERHOURS,
        secret=secret,
    )
