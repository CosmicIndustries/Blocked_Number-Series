# Blocked Number Series

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-Unlicense-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-54%20passed-brightgreen)]()

Validate phone numbers against a comprehensive dataset of blocked, reserved, and special-use number series across 15+ countries.

## Features

- **6 match types** — prefix, suffix, contains, exact, range, pattern
- **8 categories** — toll-free, emergency, reserved, premium, special, unassigned, blocked, spam
- **15+ regions** — US, CA, GB, AU, NZ, IN, DE, FR, BR, JP, RU, ZA, and Global/ITU
- **Region filtering** — restrict validation to specific countries; GLOBAL rules always apply
- **Batch validation** — validate lists of numbers in one call
- **Rich results** — matched rules, categories, reasons, serialisable to JSON
- **CLI** — pipe-friendly command-line interface with JSON output mode
- **Zero dependencies** — stdlib only

---

## Installation

```bash
pip install blocked-number-series
```

Or install from source:

```bash
git clone https://github.com/CosmicIndustries/Blocked_Number-Series
cd Blocked_Number-Series
pip install -e ".[dev]"
```

---

## Library Usage

### Basic

```python
from blocked_numbers import Validator

v = Validator()

result = v.validate("+1 (800) 555-1234")
print(result.is_blocked)       # True
print(result.primary_reason)   # "US/CA toll-free 800 series"
print(result.categories)       # {<MatchCategory.TOLL_FREE: 'toll_free'>}
```

### Batch

```python
numbers = ["+1 800 555 1234", "12025551234", "911", "0800 123 456"]
results = v.validate_batch(numbers)

for r in results:
    status = "BLOCKED" if r.is_blocked else "OK"
    print(f"{r.number:<20} [{status}]  {r.primary_reason or ''}")
```

### Region filtering

```python
# Only apply US and CA rules (plus always-on GLOBAL rules)
v_us = Validator(regions=["US", "CA"])
v_us.is_blocked("08001234567")   # False — GB rule excluded
v_us.is_blocked("112")           # True  — GLOBAL rule always applies
```

### Custom dataset

```python
v = Validator(data_path="/path/to/my_rules.json")
```

### Rich result object

```python
result = v.validate("18005551234")
print(result.as_dict())
# {
#   "number": "18005551234",
#   "is_blocked": true,
#   "reasons": ["US/CA toll-free 800 series"],
#   "categories": ["toll_free"],
#   "rules": [{"id": "US-TF-800", "region": "US", ...}]
# }
```

---

## CLI Usage

```
validate_number [OPTIONS] <number> [<number> ...]
validate_number [OPTIONS] --batch <file>

Options:
  -b, --batch FILE       Text file with one number per line
  -d, --data  FILE       Custom JSON rules file
  -r, --region CC        Restrict to region code (repeatable: -r US -r CA)
  --json                 Output as JSON array
  --blocked-only         Only print blocked numbers
  -v, --verbose          Increase log verbosity (-v, -vv)
```

### Examples

```bash
# Single number
validate_number "+1 800 555 1234"
# 18005551234          [BLOCKED]  — US/CA toll-free 800 series

# Multiple numbers
validate_number 911 12025551234 18885551234

# JSON output
validate_number --json 911 12025551234 | python -m json.tool

# Batch from file
validate_number --batch numbers.txt --blocked-only

# US/CA only
validate_number -r US -r CA 0800123456
```

---

## Data Format

Rules live in `data/blocked_numbers.json`. Add your own:

```json
{
  "rules": [
    {
      "id":          "MY-CUSTOM-001",
      "region":      "US",
      "match_type":  "prefix",
      "value":       "1999",
      "category":    "premium",
      "description": "My custom premium range",
      "tags":        ["custom"]
    }
  ]
}
```

### Match types

| Type      | Behaviour                                              |
|-----------|--------------------------------------------------------|
| `prefix`  | Number starts with `value` (digits only)               |
| `suffix`  | Number ends with `value`                               |
| `contains`| Number contains `value` anywhere                       |
| `exact`   | Number equals `value` exactly                          |
| `range`   | `value` is `"START-END"`; matches on numeric prefix    |
| `pattern` | `value` is a digit string; `X` is a wildcard digit     |

### Categories

`toll_free` · `emergency` · `reserved` · `premium` · `special` · `unassigned` · `blocked` · `spam`

---

## Development

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
```

54 tests across 9 test classes covering normalisation, all 6 match types, region filtering, batch validation, result serialisation, and sample data regression.

---

## Project Structure

```
Blocked_Number-Series/
├── blocked_numbers/        # Library package
│   ├── __init__.py         # Public API
│   ├── models.py           # NumberRule, ValidationResult, enums
│   ├── loader.py           # JSON loader + regex compiler
│   ├── validator.py        # Validator engine + normalise()
│   └── cli.py              # CLI entrypoint
├── data/
│   ├── blocked_numbers.json  # Rule dataset (70+ rules, 15+ regions)
│   └── sample_numbers.json   # Sample test numbers
├── tests/
│   └── test_validator.py   # 54 pytest tests
└── pyproject.toml
```

---

## License

[Unlicense](LICENSE) — public domain.
