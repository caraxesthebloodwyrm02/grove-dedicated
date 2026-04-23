"""Chain executor: runs tailing chain within single async context."""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from grid.tailing.chain import OnModeChange, TailingChain


class ChainExecutor:
    """Executes a TailingChain within a single async context.

    Rules:
    - R1: Strict sequence; call N+1 runs only after call N completes
    - R2: Output of N becomes input of N+1
    - R3: Call N+1 runs only when its trigger fires
    - R4: Entire chain runs in one async context (no cross-task tailing)
    - R5: On mode boundary cross, re-evaluate chain against new mode
    """

    def __init__(self, chain: TailingChain):
        self._chain = chain

    async def run(self, initial_input: Any) -> Any:
        """Run the chain with initial input.

        Args:
            initial_input: Input for the first step

        Returns:
            Output of the last step that ran, or initial_input if no steps ran
        """
        from grid.temporal_safety.context import get_temporal_context

        steps = self._chain.steps()
        if not steps:
            return initial_input

        # R5: Initialize OnModeChange.initial_mode at chain start (all instances)
        ctx_start = get_temporal_context()
        for step in steps:
            if isinstance(step.trigger, OnModeChange) and step.trigger.initial_mode is None:
                if ctx_start is not None:
                    step.trigger.initial_mode = ctx_start.mode

        output = initial_input
        error: Optional[Exception] = None

        for step in steps:
            trigger = step.trigger

            # R3: Evaluate trigger
            if not trigger.should_fire(output, error):
                break

            # R1, R2: Execute step, pass prior output as input
            try:
                result = step.call(output)
                if asyncio.iscoroutine(result):
                    result = await result
                output = result
                error = None
            except Exception as e:
                error = e
                raise

        return output
