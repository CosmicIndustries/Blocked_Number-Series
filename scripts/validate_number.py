import json
import sys
import re

Load data
with open('../data/blocked_numbers.json', 'r') as f:
    data = json.load(f)

def check_starts_with(number):
    for entry in data.get('starts_with', []):
        for prefix in entry['ranges']:
            if number.startswith(prefix):
                return True, f"Starts with {prefix} ({entry['region']})"
    return False, ""

def check_contains(number):
    for entry in data.get('contains', []):
        for pattern in entry['patterns']:
            regex_pattern = pattern.replace('XXX', '\\d{3,4}')
            if re.match(regex_pattern, number):
                return True, f"Contains pattern {pattern} ({entry['region']})"
    return False, ""

def check_ends_with(number):
    for entry in data.get('ends_with', []):
        for suffix in entry['patterns']:
            regex_pattern = suffix.replace('XXX', '\\d{3,4}')
            if re.search(regex_pattern + '$', number):
                return True, f"Ends with {suffix} ({entry['region']})"
    return False, ""

def check_reserved(number):
    for entry in data.get('reserved', []):
        for range_prefix in entry['ranges']:
            if number.startswith(range_prefix):
                return True, f"Reserved range {range_prefix} ({entry['region']})"
    return False, ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_number.py ")
        sys.exit(1)
    number_input = sys.argv[1]
    number = re.sub(r'\D', '', number_input)  # strip non-digits

    results = []

    start_chk, detail_start = check_starts_with(number)
    if start_chk:
        results.append(f"Blocked: {detail_start}")

    contain_chk, detail_contain = check_contains(number)
    if contain_chk:
        results.append(f"Blocked: {detail_contain}")

    end_chk, detail_end = check_ends_with(number)
    if end_chk:
        results.append(f"Blocked: {detail_end}")

    reserved_chk, detail_reserved = check_reserved(number)
    if reserved_chk:
        results.append(f"Reserved: {detail_reserved}")

    if results:
        print(f"Number {number_input} is BLOCKED or RESERVED:")
        for res in results:
            print(f" - {res}")
    else:
        print(f"Number {number_input} is NOT blocked or reserved.")

if name == "main":
    main()
