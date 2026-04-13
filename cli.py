"""
Blocked Number Series — CLI
"""
from __future__ import annotations

import argparse
import json
import sys
import logging
from pathlib import Path

from .validator import Validator


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="validate_number",
        description=(
            "Check phone numbers against the Blocked Number Series dataset.\n"
            "Numbers may be in any common format (+1-800-555-1234, 18005551234, etc.)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("numbers", nargs="*", metavar="NUMBER",
                   help="Phone numbers to validate.")
    p.add_argument("-b", "--batch", metavar="FILE", type=Path,
                   help="Text file with one number per line.")
    p.add_argument("-d", "--data", metavar="FILE", type=Path, default=None,
                   help="Custom JSON rules file.")
    p.add_argument("-r", "--region", metavar="CC", action="append", dest="regions",
                   help="Restrict to region code (repeatable: -r US -r CA).")
    p.add_argument("--json", action="store_true",
                   help="Output results as JSON.")
    p.add_argument("--blocked-only", action="store_true",
                   help="Only print blocked numbers.")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p


def _setup_logging(verbosity: int) -> None:
    level = {0: logging.WARNING, 1: logging.INFO}.get(verbosity, logging.DEBUG)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def _collect_numbers(args: argparse.Namespace) -> list[str]:
    numbers = list(args.numbers)
    if args.batch:
        if not args.batch.exists():
            print(f"error: batch file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)
        with args.batch.open() as fh:
            numbers.extend(line.strip() for line in fh if line.strip())
    return numbers


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args   = parser.parse_args(argv)
    _setup_logging(args.verbose)

    numbers = _collect_numbers(args)
    if not numbers:
        parser.print_help()
        return 0

    try:
        validator = Validator(data_path=args.data, regions=args.regions)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    results = validator.validate_batch(numbers)
    if args.blocked_only:
        results = [r for r in results if r.is_blocked]

    if args.json:
        print(json.dumps([r.as_dict() for r in results], indent=2))
        return 0

    for result in results:
        status = "BLOCKED" if result.is_blocked else "OK"
        line   = f"{result.number:<22} [{status}]"
        if result.is_blocked:
            line += f"  — {result.primary_reason}"
        print(line)

    blocked_count = sum(1 for r in results if r.is_blocked)
    if len(results) > 1:
        print(f"\n{blocked_count}/{len(results)} numbers blocked.")

    return 0 if blocked_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
