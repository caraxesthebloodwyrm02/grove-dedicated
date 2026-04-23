"""Tests for wyrm_sort functionality."""

from src.light_of_the_seven.sorting import SortResult, wyrm_sort


class TestWyrmSort:
    """Test suite for wyrm_sort function."""

    def test_priority_sort_descending(self):
        """Test sorting by priority key in descending order."""
        data = [
            {"priority": 3, "name": "high"},
            {"priority": 1, "name": "low"},
            {"priority": 2, "name": "medium"},
        ]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert [x["priority"] for x in result.data] == [3, 2, 1]
        assert 'Sorted by item["priority"] descending' in result.assumptions

    def test_tuple_sort_lexicographic(self):
        """Test lexicographic sorting of tuples."""
        data = [(3, "c"), (1, "a"), (2, "b")]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert result.data == [(1, "a"), (2, "b"), (3, "c")]
        assert "Lexicographic tuple sort" in result.assumptions

    def test_tuple_sort_mixed_lengths(self):
        """Test sorting tuples of different lengths."""
        data = [(1, 2, 3), (1, 2), (1,)]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert result.data == [(1,), (1, 2), (1, 2, 3)]
        assert "Mixed tuple lengths; sorted by length then lexicographically" in result.assumptions

    def test_string_sort_case_insensitive(self):
        """Test case-insensitive string sorting."""
        data = ["Banana", "apple", "Cherry"]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert result.data == ["apple", "Banana", "Cherry"]
        assert "Case-insensitive string sort" in result.assumptions

    def test_mixed_types_fallback(self):
        """Test fallback sorting for mixed types."""
        data = [42, "string", {"key": "value"}]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert len(result.data) == 3
        assert "Mixed types fallback via stable string representation" in result.assumptions

    def test_empty_list(self):
        """Test sorting empty list."""
        data = []
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert result.data == []
        assert len(result.assumptions) >= 1

    def test_single_element(self):
        """Test sorting list with single element."""
        data = [{"priority": 1}]
        result = wyrm_sort(data)
        assert isinstance(result, SortResult)
        assert result.data == [{"priority": 1}]
        assert len(result.assumptions) >= 1

    def test_reverse_sorting(self):
        """Test reverse sorting functionality."""
        data = [1, 2, 3]
        result = wyrm_sort(data, reverse=True)
        assert isinstance(result, SortResult)
        assert result.data == [3, 2, 1]

    def test_key_function_sorting(self):
        """Test custom key function sorting."""
        data = [{"value": 3}, {"value": 1}, {"value": 2}]
        result = wyrm_sort(data, key=lambda x: x["value"])
        assert isinstance(result, SortResult)
        assert [x["value"] for x in result.data] == [1, 2, 3]

    def test_key_and_reverse_combined(self):
        """Test combining key function with reverse sorting."""
        data = [{"value": 3}, {"value": 1}, {"value": 2}]
        result = wyrm_sort(data, key=lambda x: x["value"], reverse=True)
        assert isinstance(result, SortResult)
        assert [x["value"] for x in result.data] == [3, 2, 1]

    def test_assumptions_tracking(self):
        """Test that assumptions are properly tracked."""
        data = [{"priority": 1}]
        result = wyrm_sort(data)
        assert isinstance(result.assumptions, list)
        assert len(result.assumptions) > 0
        assert all(isinstance(assumption, str) for assumption in result.assumptions)

    def test_complex_nested_structures(self):
        """Test sorting complex nested structures."""
        data = [
            {"data": {"nested": {"priority": 3}}},
            {"data": {"nested": {"priority": 1}}},
            {"data": {"nested": {"priority": 2}}},
        ]
        result = wyrm_sort(data, key=lambda x: x["data"]["nested"]["priority"])
        assert isinstance(result, SortResult)
        assert [x["data"]["nested"]["priority"] for x in result.data] == [1, 2, 3]
