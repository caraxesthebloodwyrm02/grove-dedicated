"""Organization and user models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from pydantic import BaseModel, Field


class OrganizationRole(str, Enum):
    """Organization roles."""

    OPENAI = "openai"
    NVIDIA = "nvidia"
    WALT_DISNEY_PICTURES = "walt_disney_pictures"
    PARTNER = "partner"
    CUSTOMER = "customer"
    INTERNAL = "internal"


class UserRole(str, Enum):
    """User roles within an organization."""

    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"
    GUEST = "guest"


class UserStatus(str, Enum):
    """User account status."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    PENDING = "pending"
    INACTIVE = "inactive"


class OrganizationSettings(BaseModel):
    """Organization-specific settings."""

    # Focus areas
    primary_focus: List[str] = Field(default_factory=list, description="Primary focus areas")
    deep_focus: Optional[str] = Field(
        default=None, description="Deep focus area (e.g., Walt Disney Pictures)"
    )

    # Access control
    allowed_features: Set[str] = Field(default_factory=set, description="Allowed features")
    restricted_features: Set[str] = Field(default_factory=set, description="Restricted features")

    # Resource limits
    max_users: Optional[int] = Field(default=None, description="Maximum number of users")
    max_operations_per_hour: Optional[int] = Field(
        default=None, description="Rate limit for operations"
    )
    max_storage_gb: Optional[float] = Field(default=None, description="Storage limit in GB")

    # Custom prompts
    default_prompts: Dict[str, str] = Field(
        default_factory=dict, description="Default custom prompts"
    )
    prompt_templates: Dict[str, str] = Field(default_factory=dict, description="Prompt templates")

    # Discipline settings
    strict_mode: bool = Field(default=False, description="Enable strict rule enforcement")
    auto_penalty: bool = Field(default=True, description="Automatically apply penalties")

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Organization(BaseModel):
    """Organization model."""

    org_id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique organization identifier"
    )
    name: str = Field(description="Organization name")
    role: OrganizationRole = Field(description="Organization role")
    domain: Optional[str] = Field(default=None, description="Organization domain")

    # Settings
    settings: OrganizationSettings = Field(
        default_factory=OrganizationSettings, description="Organization settings"
    )

    # Membership
    user_ids: Set[str] = Field(default_factory=set, description="User IDs in this organization")
    admin_user_ids: Set[str] = Field(default_factory=set, description="Admin user IDs")

    # Status
    active: bool = Field(default=True, description="Whether organization is active")
    suspended: bool = Field(default=False, description="Whether organization is suspended")

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        """Pydantic config."""

        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat(), set: list}

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def add_user(self, user_id: str, is_admin: bool = False) -> None:
        """Add a user to the organization."""
        self.user_ids.add(user_id)
        if is_admin:
            self.admin_user_ids.add(user_id)
        self.update_timestamp()

    def remove_user(self, user_id: str) -> None:
        """Remove a user from the organization."""
        self.user_ids.discard(user_id)
        self.admin_user_ids.discard(user_id)
        self.update_timestamp()

    def is_admin(self, user_id: str) -> bool:
        """Check if user is an admin."""
        return user_id in self.admin_user_ids


class User(BaseModel):
    """User model."""

    user_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique user identifier")
    username: str = Field(description="Username")
    email: Optional[str] = Field(default=None, description="Email address")

    # Organization membership
    org_id: Optional[str] = Field(default=None, description="Primary organization ID")
    org_ids: Set[str] = Field(
        default_factory=set, description="All organization IDs user belongs to"
    )
    role: UserRole = Field(default=UserRole.VIEWER, description="User role")

    # Status
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="User status")

    # Custom prompts
    custom_prompts: Dict[str, str] = Field(default_factory=dict, description="User custom prompts")
    prompt_preferences: Dict[str, Any] = Field(
        default_factory=dict, description="Prompt preferences"
    )

    # Discipline
    violation_count: int = Field(default=0, description="Number of rule violations")
    penalty_points: float = Field(default=0.0, description="Accumulated penalty points")
    last_violation: Optional[datetime] = Field(default=None, description="Last violation timestamp")

    # Activity
    last_active: Optional[datetime] = Field(default=None, description="Last active timestamp")
    total_operations: int = Field(default=0, description="Total operations performed")

    # Metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        """Pydantic config."""

        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat(), set: list}

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def add_org(self, org_id: str) -> None:
        """Add user to an organization."""
        self.org_ids.add(org_id)
        if not self.org_id:
            self.org_id = org_id
        self.update_timestamp()

    def remove_org(self, org_id: str) -> None:
        """Remove user from an organization."""
        self.org_ids.discard(org_id)
        if self.org_id == org_id:
            self.org_id = next(iter(self.org_ids)) if self.org_ids else None
        self.update_timestamp()

    def record_violation(self, points: float) -> None:
        """Record a rule violation."""
        self.violation_count += 1
        self.penalty_points += points
        self.last_violation = datetime.now(timezone.utc)
        self.update_timestamp()

    def update_activity(self) -> None:
        """Update last active timestamp."""
        self.last_active = datetime.now(timezone.utc)
        self.total_operations += 1
        self.update_timestamp()
