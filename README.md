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

py'
    python scripts/validate_number.py

## Example:
py'
python scripts/validate_number.py 18005551234

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
