"""CLI entry point with tracing and context."""

from typing import Any, Dict, Optional

from grid.organization.org_manager import OrganizationManager
from grid.tracing import TraceManager, TraceOrigin, get_trace_manager


class CLIEntryPoint:
    """Optimized CLI entry point with tracing and context."""

    def __init__(
        self,
        trace_manager: Optional[TraceManager] = None,
        org_manager: Optional[OrganizationManager] = None,
    ):
        """Initialize CLI entry point.

        Args:
            trace_manager: Optional trace manager
            org_manager: Optional organization manager
        """
        self.trace_manager = trace_manager or get_trace_manager()
        self.org_manager = org_manager or OrganizationManager()

    def handle_command(
        self,
        command: str,
        args: Dict[str, Any],
        user_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handle a CLI command with full tracing.

        Args:
            command: Command name
            args: Command arguments
            user_id: Optional user ID
            org_id: Optional organization ID

        Returns:
            Command result
        """
        # Create trace
        with self.trace_manager.trace_action(
            action_type="cli_command",
            action_name=command,
            origin=TraceOrigin.USER_INPUT,
            user_id=user_id,
            org_id=org_id,
            input_data=args,
        ) as trace:
            # Check permissions
            if user_id and not self.org_manager.check_user_permission(user_id, command, org_id):
                trace.complete(success=False, error="Permission denied")
                return {"success": False, "error": "Permission denied"}

            # Record activity
            if user_id:
                self.org_manager.record_user_activity(user_id)

            # Process command
            try:
                result = self._process_command(command, args, trace)
                trace.complete(success=True, output_data=result)
                return {"success": True, "data": result, "trace_id": trace.trace_id}
            except Exception as e:
                trace.complete(success=False, error=str(e))
                raise

    def _process_command(
        self,
        command: str,
        args: Dict[str, Any],
        trace: Any,
    ) -> Dict[str, Any]:
        """Process a command.

        Args:
            command: Command name
            args: Command arguments
            trace: Action trace

        Returns:
            Command result
        """
        # This would delegate to appropriate service
        # For now, return placeholder
        return {"command": command, "processed": True}
