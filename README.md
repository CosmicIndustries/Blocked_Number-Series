# Blocked_Number-Series
Full JSON datasets with extensive number ranges and patterns. Validated Python script for number checking.
  Blocked Number Series Dataset & Validator

This repository contains comprehensive data of blocked, reserved, and special-use phone number series across various regions, along with a Python validator script.

##Files

data/blocked_numbers.json: JSON data of number ranges/patterns.
data/sample_numbers.json: Sample test numbers.
scripts/validate_number.py: Python script to check if a number is blocked.

##Usage

Ensure Python 3 is installed.
Save all files in the same directory structure:
  
   |-- data/
   |-- scripts/
   Run validation:
bash
python scripts/validate_number.py

##Example:
bash
python scripts/validate_number.py 18005551234

###Extending

Add more data to blocked_numbers.json as needed.
