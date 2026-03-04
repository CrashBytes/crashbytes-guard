# crashbytes-guard

Expressive guard clauses for Python — fail fast with readable validation.

## Install

```bash
pip install crashbytes-guard
```

## Usage

```python
from crashbytes_guard import Guard

def create_user(name: str, age: int, email: str) -> None:
    Guard.against_none_or_whitespace(name, "name")
    Guard.against_out_of_range(age, 0, 150, "age")
    Guard.against_invalid_email(email, "email")
    # ...proceed safely
```

## Available Guards

| Method | Description |
|--------|-------------|
| `against_none(value, name)` | Rejects `None` |
| `against_none_or_empty(value, name)` | Rejects `None` or `""` |
| `against_none_or_whitespace(value, name)` | Rejects `None`, `""`, or whitespace-only |
| `against_empty(value, name)` | Rejects empty collections/strings |
| `against_negative(value, name)` | Rejects negative numbers |
| `against_negative_or_zero(value, name)` | Rejects non-positive numbers |
| `against_zero(value, name)` | Rejects zero |
| `against_out_of_range(value, min, max, name)` | Rejects values outside `[min, max]` |
| `against_invalid_email(value, name)` | Rejects invalid email format |
| `against_invalid_url(value, name)` | Rejects non-HTTP(S) URLs |
| `against_predicate(value, pred, name, msg)` | Rejects when predicate returns `True` |
| `against_length_out_of_range(value, min, max, name)` | Rejects strings outside length range |
| `against_type(value, expected, name)` | Rejects wrong types |
| `against_not_in(value, allowed, name)` | Rejects values not in allowed set |
| `against_pattern(value, pattern, name)` | Rejects strings not matching regex |

All methods return the validated value for fluent chaining.

## License

MIT
