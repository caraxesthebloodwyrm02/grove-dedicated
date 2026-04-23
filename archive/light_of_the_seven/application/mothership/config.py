"""
Mothership Cockpit Configuration Module.

Centralized configuration management for the Mothership Cockpit
local integration backend. Supports environment-based configuration,
validation, and hierarchical settings structure.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional


class Environment(str, Enum):
    """Deployment environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def _parse_bool(value: Optional[str], default: bool = False) -> bool:
    """Parse boolean from environment variable string."""
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y", "on"}


def _parse_list(value: Optional[str], separator: str = ",") -> List[str]:
    """Parse comma-separated list from environment variable."""
    if not value:
        return []
    return [item.strip() for item in value.split(separator) if item.strip()]


@dataclass
class ServerSettings:
    """HTTP server configuration."""

    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 4
    reload: bool = False
    debug: bool = False
    root_path: str = ""
    proxy_headers: bool = True

    @classmethod
    def from_env(cls) -> "ServerSettings":
        """Load server settings from environment variables."""
        env = os.environ
        return cls(
            host=env.get("MOTHERSHIP_HOST", "0.0.0.0"),
            port=int(env.get("MOTHERSHIP_PORT", "8080")),
            workers=int(env.get("MOTHERSHIP_WORKERS", "4")),
            reload=_parse_bool(env.get("MOTHERSHIP_RELOAD")),
            debug=_parse_bool(env.get("MOTHERSHIP_DEBUG")),
            root_path=env.get("MOTHERSHIP_ROOT_PATH", ""),
            proxy_headers=_parse_bool(env.get("MOTHERSHIP_PROXY_HEADERS"), True),
        )


@dataclass
class DatabaseSettings:
    """Database connection configuration."""

    url: str = "sqlite:///./mothership.db"
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    echo: bool = False

    # Redis for caching/pubsub
    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = False

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        """Load database settings from environment variables."""
        env = os.environ
        return cls(
            url=env.get("MOTHERSHIP_DATABASE_URL", "sqlite:///./mothership.db"),
            pool_size=int(env.get("MOTHERSHIP_DB_POOL_SIZE", "5")),
            max_overflow=int(env.get("MOTHERSHIP_DB_MAX_OVERFLOW", "10")),
            pool_timeout=int(env.get("MOTHERSHIP_DB_POOL_TIMEOUT", "30")),
            echo=_parse_bool(env.get("MOTHERSHIP_DB_ECHO")),
            redis_url=env.get("MOTHERSHIP_REDIS_URL", "redis://localhost:6379/0"),
            redis_enabled=_parse_bool(env.get("MOTHERSHIP_REDIS_ENABLED")),
        )


@dataclass
class SecuritySettings:
    """Security and authentication configuration."""

    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    api_key_header: str = "X-API-Key"
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = True
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    @classmethod
    def from_env(cls) -> "SecuritySettings":
        """Load security settings from environment variables."""
        env = os.environ
        return cls(
            secret_key=env.get("MOTHERSHIP_SECRET_KEY", ""),
            algorithm=env.get("MOTHERSHIP_JWT_ALGORITHM", "HS256"),
            access_token_expire_minutes=int(
                env.get("MOTHERSHIP_ACCESS_TOKEN_EXPIRE", "30")
            ),
            refresh_token_expire_days=int(
                env.get("MOTHERSHIP_REFRESH_TOKEN_EXPIRE", "7")
            ),
            api_key_header=env.get("MOTHERSHIP_API_KEY_HEADER", "X-API-Key"),
            cors_origins=_parse_list(env.get("MOTHERSHIP_CORS_ORIGINS", "*")),
            cors_allow_credentials=_parse_bool(
                env.get("MOTHERSHIP_CORS_CREDENTIALS"), True
            ),
            rate_limit_enabled=_parse_bool(
                env.get("MOTHERSHIP_RATE_LIMIT_ENABLED"), True
            ),
            rate_limit_requests=int(env.get("MOTHERSHIP_RATE_LIMIT_REQUESTS", "100")),
            rate_limit_window_seconds=int(
                env.get("MOTHERSHIP_RATE_LIMIT_WINDOW", "60")
            ),
        )

    def validate(self) -> List[str]:
        """Validate security settings."""
        issues = []
        if not self.secret_key:
            issues.append("MOTHERSHIP_SECRET_KEY is not set - using insecure default")
        if len(self.secret_key) < 32:
            issues.append("Secret key should be at least 32 characters")
        return issues


@dataclass
class IntegrationSettings:
    """External integration configuration."""

    # Gemini Cloud Integration
    gemini_enabled: bool = True
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    gemini_timeout: int = 120

    # Grid Core Integration
    grid_api_url: str = "http://localhost:8000"
    grid_api_key: str = ""
    grid_timeout: int = 30

    # Webhook Configuration
    webhook_enabled: bool = False
    webhook_endpoints: List[str] = field(default_factory=list)
    webhook_timeout: int = 10
    webhook_retry_count: int = 3

    @classmethod
    def from_env(cls) -> "IntegrationSettings":
        """Load integration settings from environment variables."""
        env = os.environ
        return cls(
            gemini_enabled=_parse_bool(env.get("MOTHERSHIP_GEMINI_ENABLED")),
            gemini_api_key=env.get("GEMINI_API_KEY", ""),
            gemini_model=env.get("GEMINI_MODEL", "gemini-1.5-pro"),
            gemini_timeout=int(env.get("GEMINI_TIMEOUT", "120")),
            grid_api_url=env.get("GRID_API_URL", "http://localhost:8000"),
            grid_api_key=env.get("GRID_API_KEY", ""),
            grid_timeout=int(env.get("GRID_TIMEOUT", "30")),
            webhook_enabled=_parse_bool(env.get("MOTHERSHIP_WEBHOOK_ENABLED")),
            webhook_endpoints=_parse_list(env.get("MOTHERSHIP_WEBHOOK_ENDPOINTS", "")),
            webhook_timeout=int(env.get("MOTHERSHIP_WEBHOOK_TIMEOUT", "10")),
            webhook_retry_count=int(env.get("MOTHERSHIP_WEBHOOK_RETRY", "3")),
        )


@dataclass
class TelemetrySettings:
    """Telemetry and monitoring configuration."""

    enabled: bool = True
    metrics_enabled: bool = True
    metrics_path: str = "/metrics"
    tracing_enabled: bool = False
    tracing_sample_rate: float = 0.1
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "json"
    log_file: Optional[str] = None
    health_check_interval: int = 30

    @classmethod
    def from_env(cls) -> "TelemetrySettings":
        """Load telemetry settings from environment variables."""
        env = os.environ
        log_level_str = env.get("MOTHERSHIP_LOG_LEVEL", "INFO").upper()
        try:
            log_level = LogLevel(log_level_str)
        except ValueError:
            log_level = LogLevel.INFO

        return cls(
            enabled=_parse_bool(env.get("MOTHERSHIP_TELEMETRY_ENABLED"), True),
            metrics_enabled=_parse_bool(env.get("MOTHERSHIP_METRICS_ENABLED"), True),
            metrics_path=env.get("MOTHERSHIP_METRICS_PATH", "/metrics"),
            tracing_enabled=_parse_bool(env.get("MOTHERSHIP_TRACING_ENABLED")),
            tracing_sample_rate=float(env.get("MOTHERSHIP_TRACING_SAMPLE_RATE", "0.1")),
            log_level=log_level,
            log_format=env.get("MOTHERSHIP_LOG_FORMAT", "json"),
            log_file=env.get("MOTHERSHIP_LOG_FILE"),
            health_check_interval=int(
                env.get("MOTHERSHIP_HEALTH_CHECK_INTERVAL", "30")
            ),
        )


@dataclass
class CockpitSettings:
    """Cockpit-specific operational settings."""

    # Session management
    session_timeout_minutes: int = 60
    max_concurrent_sessions: int = 100

    # Task management
    task_queue_size: int = 1000
    task_timeout_seconds: int = 300
    task_retry_limit: int = 3

    # Real-time features
    websocket_enabled: bool = True
    websocket_heartbeat_interval: int = 30
    websocket_max_connections: int = 500

    # Dashboard features
    dashboard_refresh_rate: int = 5
    dashboard_history_hours: int = 24

    # Auto-scaling thresholds
    autoscale_enabled: bool = False
    autoscale_min_workers: int = 1
    autoscale_max_workers: int = 10
    autoscale_cpu_threshold: float = 0.8

    @classmethod
    def from_env(cls) -> "CockpitSettings":
        """Load cockpit settings from environment variables."""
        env = os.environ
        return cls(
            session_timeout_minutes=int(env.get("MOTHERSHIP_SESSION_TIMEOUT", "60")),
            max_concurrent_sessions=int(env.get("MOTHERSHIP_MAX_SESSIONS", "100")),
            task_queue_size=int(env.get("MOTHERSHIP_TASK_QUEUE_SIZE", "1000")),
            task_timeout_seconds=int(env.get("MOTHERSHIP_TASK_TIMEOUT", "300")),
            task_retry_limit=int(env.get("MOTHERSHIP_TASK_RETRY_LIMIT", "3")),
            websocket_enabled=_parse_bool(
                env.get("MOTHERSHIP_WEBSOCKET_ENABLED"), True
            ),
            websocket_heartbeat_interval=int(env.get("MOTHERSHIP_WS_HEARTBEAT", "30")),
            websocket_max_connections=int(
                env.get("MOTHERSHIP_WS_MAX_CONNECTIONS", "500")
            ),
            dashboard_refresh_rate=int(env.get("MOTHERSHIP_DASHBOARD_REFRESH", "5")),
            dashboard_history_hours=int(env.get("MOTHERSHIP_DASHBOARD_HISTORY", "24")),
            autoscale_enabled=_parse_bool(env.get("MOTHERSHIP_AUTOSCALE_ENABLED")),
            autoscale_min_workers=int(env.get("MOTHERSHIP_AUTOSCALE_MIN", "1")),
            autoscale_max_workers=int(env.get("MOTHERSHIP_AUTOSCALE_MAX", "10")),
            autoscale_cpu_threshold=float(
                env.get("MOTHERSHIP_AUTOSCALE_CPU_THRESHOLD", "0.8")
            ),
        )


@dataclass
class MothershipSettings:
    """
    Top-level Mothership Cockpit configuration.

    Aggregates all configuration subsystems into a single,
    easy-to-use settings object with validation support.
    """

    app_name: str = "Mothership Cockpit"
    app_version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    base_path: Path = field(default_factory=lambda: Path.cwd())

    # Subsystem settings
    server: ServerSettings = field(default_factory=ServerSettings.from_env)
    database: DatabaseSettings = field(default_factory=DatabaseSettings.from_env)
    security: SecuritySettings = field(default_factory=SecuritySettings.from_env)
    integrations: IntegrationSettings = field(
        default_factory=IntegrationSettings.from_env
    )
    telemetry: TelemetrySettings = field(default_factory=TelemetrySettings.from_env)
    cockpit: CockpitSettings = field(default_factory=CockpitSettings.from_env)

    @classmethod
    def from_env(cls) -> "MothershipSettings":
        """Load all settings from environment variables."""
        env = os.environ
        env_str = env.get("MOTHERSHIP_ENVIRONMENT", "development").lower()
        try:
            environment = Environment(env_str)
        except ValueError:
            environment = Environment.DEVELOPMENT

        base_path_str = env.get("MOTHERSHIP_BASE_PATH")
        base_path = Path(base_path_str) if base_path_str else Path.cwd()

        return cls(
            app_name=env.get("MOTHERSHIP_APP_NAME", "Mothership Cockpit"),
            app_version=env.get("MOTHERSHIP_APP_VERSION", "1.0.0"),
            environment=environment,
            base_path=base_path,
        )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION

    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.environment == Environment.TESTING

    @property
    def debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return self.server.debug or self.is_development

    def validate(self) -> List[str]:
        """Validate all settings and return list of issues."""
        issues = []

        # Security validation
        issues.extend(self.security.validate())

        # Production-specific validation
        if self.is_production:
            if self.server.debug:
                issues.append("Debug mode should be disabled in production")
            if self.server.reload:
                issues.append("Auto-reload should be disabled in production")
            if "*" in self.security.cors_origins:
                issues.append("CORS should not allow all origins in production")

        return issues

    def to_dict(self, mask_secrets: bool = True) -> Dict[str, Any]:
        """Export settings as dictionary with optional secret masking."""

        def mask_value(key: str, value: Any) -> Any:
            if not mask_secrets:
                return value
            secret_keys = {"secret_key", "api_key", "password", "token"}
            if any(s in key.lower() for s in secret_keys):
                if isinstance(value, str) and value:
                    return f"{value[:4]}***" if len(value) > 4 else "***"
            return value

        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment.value,
            "base_path": str(self.base_path),
            "debug_enabled": self.debug_enabled,
            "server": {
                "host": self.server.host,
                "port": self.server.port,
                "workers": self.server.workers,
            },
            "database": {
                "url": mask_value("url", self.database.url),
                "redis_enabled": self.database.redis_enabled,
            },
            "security": {
                "cors_origins": self.security.cors_origins,
                "rate_limit_enabled": self.security.rate_limit_enabled,
            },
            "integrations": {
                "gemini_enabled": self.integrations.gemini_enabled,
                "grid_api_url": self.integrations.grid_api_url,
                "webhook_enabled": self.integrations.webhook_enabled,
            },
            "telemetry": {
                "enabled": self.telemetry.enabled,
                "log_level": self.telemetry.log_level.value,
            },
            "cockpit": {
                "websocket_enabled": self.cockpit.websocket_enabled,
                "max_concurrent_sessions": self.cockpit.max_concurrent_sessions,
            },
        }


# Module-level singleton
_settings: Optional[MothershipSettings] = None


@lru_cache(maxsize=1)
def get_settings() -> MothershipSettings:
    """
    Get cached settings instance.

    Uses LRU cache to ensure settings are only loaded once
    and remain consistent throughout the application lifecycle.
    """
    global _settings
    if _settings is None:
        _settings = MothershipSettings.from_env()
    return _settings


def reload_settings() -> MothershipSettings:
    """Force reload settings from environment."""
    global _settings
    get_settings.cache_clear()
    _settings = MothershipSettings.from_env()
    return _settings


# Convenience export
settings = get_settings()


__all__ = [
    "MothershipSettings",
    "ServerSettings",
    "DatabaseSettings",
    "SecuritySettings",
    "IntegrationSettings",
    "TelemetrySettings",
    "CockpitSettings",
    "Environment",
    "LogLevel",
    "get_settings",
    "reload_settings",
    "settings",
]
