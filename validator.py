"""
Blocked Number Series — Validator Engine
"""
from __future__ import annotations

import re
import logging
from pathlib import Path
from typing import Iterable

from .models import MatchType, NumberRule, ValidationResult
from .loader import compile_pattern, load_rules

log = logging.getLogger(__name__)

_STRIP_RE = re.compile(r"[\s\-\(\)\+\.]")


def normalise(number: str) -> str:
    """Strip formatting characters; return digits-only string."""
    return _STRIP_RE.sub("", number)


class Validator:
    """Thread-safe phone number validator."""

    def __init__(
        self,
        rules: list[NumberRule] | None = None,
        data_path: Path | str | None = None,
        regions: Iterable[str] | None = None,
    ) -> None:
        raw_rules = rules if rules is not None else load_rules(data_path)
        if regions:
            region_set = {r.upper() for r in regions} | {"GLOBAL"}
            raw_rules = [r for r in raw_rules if r.region in region_set]
        self._rules = raw_rules
        self._compiled: list[tuple[NumberRule, re.Pattern | None]] = [
            (rule, compile_pattern(rule)) for rule in self._rules
        ]
        log.debug("Validator ready: %d rules", len(self._rules))

    def validate(self, number: str) -> ValidationResult:
        normalised = normalise(number)
        if not normalised.isdigit():
            raise ValueError(
                f"Non-digit characters after normalisation: {normalised!r}"
            )
        matched: list[NumberRule] = []
        for rule, pattern in self._compiled:
            if pattern is not None:
                if pattern.search(normalised):
                    matched.append(rule)
            elif rule.match_type == MatchType.RANGE:
                if self._in_range(normalised, rule.value):
                    matched.append(rule)
        return ValidationResult(
            number=normalised,
            is_blocked=bool(matched),
            matched_rules=tuple(matched),
            reasons=tuple(r.description for r in matched),
        )

    def validate_batch(self, numbers: Iterable[str]) -> list[ValidationResult]:
        return [self.validate(n) for n in numbers]

    def is_blocked(self, number: str) -> bool:
        return self.validate(number).is_blocked

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    @staticmethod
    def _in_range(number: str, range_spec: str) -> bool:
        try:
            start_str, end_str = range_spec.split("-", 1)
            start_str, end_str = start_str.strip(), end_str.strip()
            prefix_len = len(start_str)
            prefix = number[:prefix_len]
            if len(prefix) < prefix_len:
                return False
            return int(start_str) <= int(prefix) <= int(end_str)
        except (ValueError, TypeError):
            log.warning("Invalid range spec: %r", range_spec)
            return False
