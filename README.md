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

# BLOCKED_NUMBER-SERIES                                                   Validated Python script for number checking.
	## Full JSON datasets with extensive number ranges and patterns. Validated Python script for number checking.

##   Blocked Number Series Dataset & Validator

> 
This repository contains comprehensive data of blocked, reserved, and special-use phone number series across various regions, along with a Python validator script.

## Files

------------
- data/blocked_numbers.json: JSON data of number ranges/patterns.
- data/sample_numbers.json: Sample test numbers.
- scripts/validate_number.py: Python script to check if a number is blocked.

## Usage

Ensure Python 3 is installed.
Save all files in the same directory structure:
  
   |-- data/
   |-- scripts/
   Run validation:

```python
    python scripts/validate_number.py
```

## Example:
```python
python scripts/validate_number.py 18005551234
```
### Extending

Add more data to blocked_numbers.json as needed.


# 1. Numbers Starting With

International & Regional Examples

| Region / Country | Number Series / Prefix | Description / Usage |
|---------------------|------------------------|---------------------|
| North America | 1-800 | Toll-free service numbers in the US and Canada. |
| India | 1800 | Toll-free numbers. |
| UK | 0800 | Toll-free numbers. |
| Australia | 0800 | Toll-free numbers. |
| Germany | 0800 | Toll-free numbers. |
| Brazil | 0800 | Toll-free numbers. |
| EU | 112 | Emergency services (EU-wide). |
| Global | 000 | International reserved number for emergencies (e.g., Australia). |
| Japan | 110 | Police emergency. |
| France | 15 | Medical emergency. |

# 2. Numbers Containing

Examples of Number Series with Internal Patterns

| Region / Country | Number Series / Pattern | Description / Usage |
|---------------------|-------------------------|---------------------|
| North America | 1-800-XXX-XXXX | Toll-free with variable last 4 digits. |
| India | 1800-XXX-XXXX | Toll-free with variable last four digits. |
| UK | 0843-XXX-XXXX | Non-geographic service number. |
| Canada | 1-800-XXX-XXX | Toll-free with varied last digits. |
| Europe | 0800-XXX-XXXX | Toll-free across multiple countries. |
| Brazil | 0800-XXX-XXXX | Toll-free. |
| Australia | 1800-XXX-XXX | Toll-free. |

# 3. Numbers Ending With

Examples of Endings for Blocked / Reserved Numbers

| Region / Country | Ending Number Pattern | Usage / Notes |
|---------------------|------------------------|----------------|
| North America | XXX-XXXX ending with 0000 | Common for toll-free numbers like 1-800-0000. |
| India | XXXX ending with 000 | Toll-free numbers like 1800-XXXX-000. |
| UK | XXXX ending with 0000 | Reserved or blocked series. |
| EU | 112 | Emergency services, fixed ending. |
| Australia | 000 | Emergency contact number, reserved. |

# 4. Additional Regional & Special-Use Number Ranges

Reserved & Special Number Ranges

| Region / Country | Number Range | Usage / Notes |
|---------------------|----------------|--------------|
| Australia | 000 | Emergency services. Reserved for fire, police, ambulance. |
| New Zealand | 111 | Emergency services. |
| Russia | 112 | Emergency services. |
| South Africa | 10111 | Police emergency. |
| EU | 116000-116999 | Child helplines, reserved for special services. |
| International | 700-799 | Reserved for future or special use (ITU reserved). |
| Global | 999 | Emergency, used in some countries like UK, India. |

# 5. Special Note: Reserved & Unassigned Ranges

**ITU Reserved:**
  700-799: Reserved for future use, international telecommunication purposes.

**Unassigned / Not Allocated:**
  Many countries have ranges like 900-999 for premium-rate services or are unassigned.

**Premium Rate / Special Services:**
  900 series in US (premium-rate numbers).
  118 in UK (various special services).

# 6. Building the List Programmatically

Here's an example of how to structure this data in JSON format, extending the previous data files:

```json
{
  "starts_with": [
    {"region": "US", "ranges": ["800", "888"]},
    {"region": "IN", "ranges": ["1800"]},
    {"region": "UK", "ranges": ["0800"]},
    {"region": "AU", "ranges": ["0800", "1800"]},
    {"region": "EU", "ranges": ["112"]}
  ],
  "contains": [
    {"region": "US", "patterns": ["1-800-XXX-XXXX", "1-888-XXX-XXXX"]},
    {"region": "IN", "patterns": ["1800-XXX-XXXX"]},
    {"region": "UK", "patterns": ["0843-XXX-XXXX"]},
    {"region": "BR", "patterns": ["0800-XXX-XXXX"]},
    {"region": "AU", "patterns": ["1800-XXX-XXX"]}
  ],
  "ends_with": [
    {"region": "US", "patterns": ["XXX-0000"]},
    {"region": "IN", "patterns": ["XXXX-000"]},
    {"region": "UK", "patterns": ["XXXX-0000"]}
  ],
  "reserved": [
    {"region": "Global", "ranges": ["000", "111", "999"]},
    {"region": "AU", "ranges": ["000"]},
    {"region": "NZ", "ranges": ["111"]}
  ]
}

```

## Summary & Next Steps

  The list can be expanded further with more region-specific data.
You can automate validation scripts to check if a number falls into any of these categories.
These structures can be stored in JSON, CSV, or database tables for easy access.

---
## License

[Unlicense](LICENSE) — public domain.
