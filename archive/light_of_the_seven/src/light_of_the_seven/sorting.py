from dataclasses import dataclass
from typing import Any, Callable, List, Optional


@dataclass
class SortResult:
    """Container for sorting results and assumptions."""

    data: List[Any]
    assumptions: List[str]


def wyrm_sort(
    data: List[Any], key: Optional[Callable[[Any], Any]] = None, reverse: bool = False
) -> SortResult:
    """
    Enhanced wyrm_sort with type hints and additional functionality.

    Args:
        data: List of items to sort
        key: Optional key function (similar to built-in sorted)
        reverse: If True, sort in descending order

    Returns:
        SortResult: Contains sorted data and list of assumptions
    """
    assumptions = []

    # Handle empty or single-element lists
    if len(data) <= 1:
        assumptions.append("Trivial case: empty or single-element list")
        return SortResult(data.copy(), assumptions)

    # Rule 1: If items expose a 'priority', sort by descending priority (higher priority first)
    if all(hasattr(item, "get") and "priority" in item for item in data) and key is None:
        # Priority sorting defaults to descending (higher priority first)
        # reverse=False => descending, reverse=True => ascending
        assumptions.append('Sorted by item["priority"] descending')
        sorted_data = sorted(data, key=lambda x: x.get("priority", 0), reverse=not reverse)
        return SortResult(sorted_data, assumptions)

    # Apply custom key function if provided
    sort_key = key if key is not None else lambda x: x

    # Rule 2: If items are tuples of equal length, sort lexicographically
    if all(isinstance(item, tuple) for item in data) and key is None:
        lengths = {len(item) for item in data}
        if len(lengths) == 1:
            assumptions.append("Lexicographic tuple sort")
            return SortResult(sorted(data, key=sort_key, reverse=reverse), assumptions)
        else:
            assumptions.append("Mixed tuple lengths; sorted by length then lexicographically")
            return SortResult(
                sorted(data, key=lambda x: (len(x), sort_key(x)), reverse=reverse), assumptions
            )

    # Rule 3: If items are strings, sort case-insensitively but stable
    if all(isinstance(item, str) for item in data) and key is None:
        assumptions.append("Case-insensitive string sort")
        return SortResult(
            sorted(data, key=lambda x: sort_key(x).lower(), reverse=reverse), assumptions
        )

    # Rule 4: Mixed types → stable stringified ordering
    assumptions.append("Mixed types fallback via stable string representation")
    return SortResult(
        sorted(data, key=lambda x: (str(type(sort_key(x))), str(sort_key(x))), reverse=reverse),
        assumptions,
    )
