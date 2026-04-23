"""Tailing chain and trigger definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, List, Optional, Union

from grid.temporal_safety.context import get_temporal_context


@dataclass
class TailingTrigger(ABC):
    """Base for trigger types that determine when the next call in a chain runs."""

    @abstractmethod
    def should_fire(
        self,
        prior_output: Any,
        prior_error: Optional[Exception],
    ) -> bool:
        """Return True if the next call should run after prior call completed."""
        ...


@dataclass
class OnCompletion(TailingTrigger):
    """Fire when prior call completes (success or defined error)."""

    def should_fire(
        self,
        prior_output: Any,
        prior_error: Optional[Exception],
    ) -> bool:
        return True


@dataclass
class OnCondition(TailingTrigger):
    """Fire when predicate(prior_output) is True."""

    predicate: Callable[[Any], bool]

    def should_fire(
        self,
        prior_output: Any,
        prior_error: Optional[Exception],
    ) -> bool:
        if prior_error is not None:
            return False
        return self.predicate(prior_output)


@dataclass
class OnModeChange(TailingTrigger):
    """Fire when operational mode differs from when chain started.

    Used to re-validate or apply hardened auth when crossing into afterhours.
    """

    initial_mode: Optional[Any] = field(default=None, repr=False)

    def should_fire(
        self,
        prior_output: Any,
        prior_error: Optional[Exception],
    ) -> bool:
        if prior_error is not None:
            return False
        ctx = get_temporal_context()
        if ctx is None:
            return False
        return ctx.mode != self.initial_mode


@dataclass
class TailingStep:
    """A single step: callable + trigger."""

    call: Union[Callable[[Any], Any], Callable[[Any], Awaitable[Any]]]
    trigger: TailingTrigger = field(default_factory=OnCompletion)


class TailingChain:
    """Ordered chain of (callable, trigger) steps."""

    def __init__(self, steps: Optional[List[TailingStep]] = None):
        self._steps: List[TailingStep] = list(steps or [])

    def append(self, call: Callable, trigger: Optional[TailingTrigger] = None) -> TailingChain:
        """Append a step. Returns self for chaining."""
        self._steps.append(TailingStep(call=call, trigger=trigger or OnCompletion()))
        return self

    def steps(self) -> List[TailingStep]:
        """Return immutable view of steps."""
        return list(self._steps)
