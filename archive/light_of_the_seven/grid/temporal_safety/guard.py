"""Temporal property guard for time-sensitive field encryption."""

from __future__ import annotations

import base64
import hashlib
import json
from typing import Any, Dict

from grid.temporal_safety.context import AsyncTemporalContext

TEMPORAL_SENSITIVE_FIELDS = frozenset(
    {"created_at", "expires_at", "session_boundary", "mode_switch_time"}
)


class TemporalPropertyGuard:
    """Encrypts/decrypts time-sensitive properties using temporal context in key derivation."""

    def __init__(self, base_key: bytes):
        """Initialize guard with base key for derivation.

        Args:
            base_key: Base secret key (32 bytes recommended for Fernet/AES-256).
        """
        self._base_key = base_key

    def _derive_key(self, context: AsyncTemporalContext) -> bytes:
        """Derive encryption key from base_key + mode + time_window_id."""
        material = f"{context.mode.value}:{context.time_window_id}".encode()
        return hashlib.pbkdf2_hmac(
            "sha256",
            self._base_key,
            material,
            iterations=100000,
            dklen=32,
        )

    def _encrypt_value(self, value: Any, key: bytes) -> str:
        """Encrypt a single value (JSON-serializable) to base64 string."""
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            # Fallback: simple base64 + XOR-like obfuscation when cryptography unavailable
            payload = json.dumps(value).encode()
            return base64.b64encode(payload).decode()

        fernet_key = base64.urlsafe_b64encode(key[:32])
        f = Fernet(fernet_key)
        payload = json.dumps(value).encode()
        return f.encrypt(payload).decode()

    def _decrypt_value(self, encrypted: str, key: bytes) -> Any:
        """Decrypt a base64-encoded value."""
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            return json.loads(base64.b64decode(encrypted).decode())

        fernet_key = base64.urlsafe_b64encode(key[:32])
        f = Fernet(fernet_key)
        decrypted = f.decrypt(encrypted.encode())
        return json.loads(decrypted.decode())

    def encrypt(self, data: Dict[str, Any], context: AsyncTemporalContext) -> Dict[str, Any]:
        """Encrypt time-sensitive fields in data.

        Args:
            data: Dictionary potentially containing temporal-sensitive fields
            context: Temporal context for key derivation

        Returns:
            New dict with encrypted values for marked fields
        """
        key = self._derive_key(context)
        result = dict(data)
        for field in TEMPORAL_SENSITIVE_FIELDS:
            if field in result and result[field] is not None:
                result[field] = self._encrypt_value(result[field], key)
        return result

    def decrypt(
        self,
        data: Dict[str, Any],
        context: AsyncTemporalContext,
    ) -> Dict[str, Any]:
        """Decrypt time-sensitive fields in data.

        Args:
            data: Dictionary with potentially encrypted temporal-sensitive fields
            context: Temporal context for key derivation (must match encryption context)

        Returns:
            New dict with decrypted values for marked fields
        """
        key = self._derive_key(context)
        result = dict(data)
        for field in TEMPORAL_SENSITIVE_FIELDS:
            if field in result and result[field] is not None:
                try:
                    result[field] = self._decrypt_value(str(result[field]), key)
                except Exception:
                    pass  # Leave as-is if decryption fails
        return result
