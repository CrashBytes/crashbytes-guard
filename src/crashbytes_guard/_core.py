"""Guard clauses for defensive programming."""

from __future__ import annotations

import re
from collections.abc import Callable, Sized
from typing import Any, TypeVar

T = TypeVar("T")

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class GuardError(ValueError):
    """Raised when a guard clause fails."""


class Guard:
    """Expressive guard clauses — fail fast with readable validation.

    Usage::

        Guard.against_none(user, "user")
        Guard.against_empty(name, "name")
        Guard.against_negative(amount, "amount")
    """

    @staticmethod
    def against_none(value: T | None, name: str = "value") -> T:
        """Raise if *value* is ``None``."""
        if value is None:
            raise GuardError(f"{name} must not be None")
        return value

    @staticmethod
    def against_none_or_empty(value: str | None, name: str = "value") -> str:
        """Raise if *value* is ``None`` or an empty string."""
        if value is None or value == "":
            raise GuardError(f"{name} must not be None or empty")
        return value

    @staticmethod
    def against_none_or_whitespace(value: str | None, name: str = "value") -> str:
        """Raise if *value* is ``None``, empty, or only whitespace."""
        if value is None or value.strip() == "":
            raise GuardError(f"{name} must not be None, empty, or whitespace")
        return value

    @staticmethod
    def against_empty(value: T, name: str = "value") -> T:
        """Raise if *value* is empty (works on strings, lists, dicts, sets, etc.)."""
        if isinstance(value, Sized) and len(value) == 0:
            raise GuardError(f"{name} must not be empty")
        return value

    @staticmethod
    def against_negative(value: int | float, name: str = "value") -> int | float:
        """Raise if *value* is negative."""
        if value < 0:
            raise GuardError(f"{name} must not be negative (got {value})")
        return value

    @staticmethod
    def against_negative_or_zero(
        value: int | float, name: str = "value"
    ) -> int | float:
        """Raise if *value* is negative or zero."""
        if value <= 0:
            raise GuardError(f"{name} must be positive (got {value})")
        return value

    @staticmethod
    def against_zero(value: int | float, name: str = "value") -> int | float:
        """Raise if *value* is zero."""
        if value == 0:
            raise GuardError(f"{name} must not be zero")
        return value

    @staticmethod
    def against_out_of_range(
        value: int | float,
        min_val: int | float,
        max_val: int | float,
        name: str = "value",
    ) -> int | float:
        """Raise if *value* is outside ``[min_val, max_val]``."""
        if value < min_val or value > max_val:
            raise GuardError(f"{name} must be between {min_val} and {max_val} (got {value})")
        return value

    @staticmethod
    def against_invalid_email(value: str, name: str = "email") -> str:
        """Raise if *value* is not a valid email address."""
        if not _EMAIL_RE.match(value):
            raise GuardError(f"{name} is not a valid email address (got {value!r})")
        return value

    @staticmethod
    def against_invalid_url(value: str, name: str = "url") -> str:
        """Raise if *value* does not start with ``http://`` or ``https://``."""
        if not value.startswith(("http://", "https://")):
            raise GuardError(f"{name} is not a valid URL (got {value!r})")
        return value

    @staticmethod
    def against_predicate(
        value: T,
        predicate: Callable[[T], bool],
        name: str = "value",
        message: str | None = None,
    ) -> T:
        """Raise if *predicate(value)* returns ``True``."""
        if predicate(value):
            msg = message or f"{name} failed guard predicate"
            raise GuardError(msg)
        return value

    @staticmethod
    def against_length_out_of_range(
        value: str,
        min_len: int,
        max_len: int,
        name: str = "value",
    ) -> str:
        """Raise if ``len(value)`` is outside ``[min_len, max_len]``."""
        if len(value) < min_len or len(value) > max_len:
            raise GuardError(
                f"{name} length must be between {min_len} and {max_len} (got {len(value)})"
            )
        return value

    @staticmethod
    def against_type(value: Any, expected: type[T], name: str = "value") -> T:
        """Raise if *value* is not an instance of *expected*."""
        if not isinstance(value, expected):
            raise GuardError(
                f"{name} must be of type {expected.__name__} "
                f"(got {type(value).__name__})"
            )
        return value

    @staticmethod
    def against_not_in(value: T, allowed: Any, name: str = "value") -> T:
        """Raise if *value* is not in *allowed*."""
        if value not in allowed:
            raise GuardError(f"{name} must be one of {allowed} (got {value!r})")
        return value

    @staticmethod
    def against_pattern(
        value: str, pattern: str, name: str = "value"
    ) -> str:
        """Raise if *value* does not match *pattern*."""
        if not re.match(pattern, value):
            raise GuardError(f"{name} must match pattern {pattern!r} (got {value!r})")
        return value
