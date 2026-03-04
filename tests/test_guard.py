"""Tests for crashbytes-guard."""

from __future__ import annotations

import pytest

from crashbytes_guard import Guard, GuardError


class TestAgainstNone:
    def test_passes_non_none(self) -> None:
        assert Guard.against_none(42, "x") == 42

    def test_returns_value(self) -> None:
        obj = object()
        assert Guard.against_none(obj) is obj

    def test_raises_on_none(self) -> None:
        with pytest.raises(GuardError, match="user must not be None"):
            Guard.against_none(None, "user")

    def test_default_name(self) -> None:
        with pytest.raises(GuardError, match="value must not be None"):
            Guard.against_none(None)


class TestAgainstNoneOrEmpty:
    def test_passes_non_empty(self) -> None:
        assert Guard.against_none_or_empty("hello", "s") == "hello"

    def test_raises_on_none(self) -> None:
        with pytest.raises(GuardError, match="must not be None or empty"):
            Guard.against_none_or_empty(None, "s")

    def test_raises_on_empty(self) -> None:
        with pytest.raises(GuardError, match="must not be None or empty"):
            Guard.against_none_or_empty("", "s")


class TestAgainstNoneOrWhitespace:
    def test_passes_non_whitespace(self) -> None:
        assert Guard.against_none_or_whitespace("hello") == "hello"

    def test_raises_on_none(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_none_or_whitespace(None)

    def test_raises_on_empty(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_none_or_whitespace("")

    def test_raises_on_whitespace(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_none_or_whitespace("   \t\n")


class TestAgainstEmpty:
    def test_passes_non_empty_list(self) -> None:
        assert Guard.against_empty([1, 2], "items") == [1, 2]

    def test_passes_non_empty_str(self) -> None:
        assert Guard.against_empty("hi") == "hi"

    def test_raises_on_empty_list(self) -> None:
        with pytest.raises(GuardError, match="items must not be empty"):
            Guard.against_empty([], "items")

    def test_raises_on_empty_dict(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_empty({}, "d")

    def test_raises_on_empty_set(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_empty(set(), "s")

    def test_raises_on_empty_str(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_empty("", "s")


class TestAgainstNegative:
    def test_passes_positive(self) -> None:
        assert Guard.against_negative(5) == 5

    def test_passes_zero(self) -> None:
        assert Guard.against_negative(0) == 0

    def test_raises_on_negative(self) -> None:
        with pytest.raises(GuardError, match="must not be negative"):
            Guard.against_negative(-1, "amount")

    def test_works_with_float(self) -> None:
        assert Guard.against_negative(0.5) == 0.5
        with pytest.raises(GuardError):
            Guard.against_negative(-0.1)


class TestAgainstNegativeOrZero:
    def test_passes_positive(self) -> None:
        assert Guard.against_negative_or_zero(1) == 1

    def test_raises_on_zero(self) -> None:
        with pytest.raises(GuardError, match="must be positive"):
            Guard.against_negative_or_zero(0, "count")

    def test_raises_on_negative(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_negative_or_zero(-5)


class TestAgainstZero:
    def test_passes_positive(self) -> None:
        assert Guard.against_zero(1) == 1

    def test_passes_negative(self) -> None:
        assert Guard.against_zero(-1) == -1

    def test_raises_on_zero(self) -> None:
        with pytest.raises(GuardError, match="must not be zero"):
            Guard.against_zero(0, "divisor")


class TestAgainstOutOfRange:
    def test_passes_in_range(self) -> None:
        assert Guard.against_out_of_range(5, 1, 10) == 5

    def test_passes_at_min(self) -> None:
        assert Guard.against_out_of_range(1, 1, 10) == 1

    def test_passes_at_max(self) -> None:
        assert Guard.against_out_of_range(10, 1, 10) == 10

    def test_raises_below_min(self) -> None:
        with pytest.raises(GuardError, match="must be between"):
            Guard.against_out_of_range(0, 1, 10, "age")

    def test_raises_above_max(self) -> None:
        with pytest.raises(GuardError, match="must be between"):
            Guard.against_out_of_range(11, 1, 10, "age")


class TestAgainstInvalidEmail:
    def test_passes_valid_email(self) -> None:
        assert Guard.against_invalid_email("user@example.com") == "user@example.com"

    def test_raises_on_missing_at(self) -> None:
        with pytest.raises(GuardError, match="not a valid email"):
            Guard.against_invalid_email("nope")

    def test_raises_on_missing_domain(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_invalid_email("user@")

    def test_raises_on_empty(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_invalid_email("")


class TestAgainstInvalidUrl:
    def test_passes_http(self) -> None:
        assert Guard.against_invalid_url("http://example.com") == "http://example.com"

    def test_passes_https(self) -> None:
        assert Guard.against_invalid_url("https://example.com") == "https://example.com"

    def test_raises_on_ftp(self) -> None:
        with pytest.raises(GuardError, match="not a valid URL"):
            Guard.against_invalid_url("ftp://example.com")

    def test_raises_on_empty(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_invalid_url("")


class TestAgainstPredicate:
    def test_passes_when_false(self) -> None:
        assert Guard.against_predicate(5, lambda x: x > 10) == 5

    def test_raises_when_true(self) -> None:
        with pytest.raises(GuardError, match="failed guard predicate"):
            Guard.against_predicate(15, lambda x: x > 10)

    def test_custom_message(self) -> None:
        with pytest.raises(GuardError, match="too big"):
            Guard.against_predicate(15, lambda x: x > 10, message="too big")


class TestAgainstLengthOutOfRange:
    def test_passes_in_range(self) -> None:
        assert Guard.against_length_out_of_range("hello", 1, 10) == "hello"

    def test_raises_too_short(self) -> None:
        with pytest.raises(GuardError, match="length must be between"):
            Guard.against_length_out_of_range("", 1, 10, "name")

    def test_raises_too_long(self) -> None:
        with pytest.raises(GuardError):
            Guard.against_length_out_of_range("a" * 20, 1, 10)


class TestAgainstType:
    def test_passes_correct_type(self) -> None:
        assert Guard.against_type(42, int) == 42

    def test_raises_wrong_type(self) -> None:
        with pytest.raises(GuardError, match="must be of type int"):
            Guard.against_type("hello", int, "count")

    def test_passes_subclass(self) -> None:
        assert Guard.against_type(True, int) is True


class TestAgainstNotIn:
    def test_passes_when_in(self) -> None:
        assert Guard.against_not_in("a", ["a", "b", "c"]) == "a"

    def test_raises_when_not_in(self) -> None:
        with pytest.raises(GuardError, match="must be one of"):
            Guard.against_not_in("d", ["a", "b", "c"], "choice")


class TestAgainstPattern:
    def test_passes_matching(self) -> None:
        assert Guard.against_pattern("abc123", r"^[a-z]+\d+$") == "abc123"

    def test_raises_non_matching(self) -> None:
        with pytest.raises(GuardError, match="must match pattern"):
            Guard.against_pattern("ABC", r"^[a-z]+$", "code")
