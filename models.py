"""
Blocked Number Series — Data Models
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MatchType(str, Enum):
    PREFIX   = "prefix"
    SUFFIX   = "suffix"
    CONTAINS = "contains"
    EXACT    = "exact"
    RANGE    = "range"
    PATTERN  = "pattern"


class MatchCategory(str, Enum):
    TOLL_FREE  = "toll_free"
    EMERGENCY  = "emergency"
    RESERVED   = "reserved"
    PREMIUM    = "premium"
    SPECIAL    = "special"
    UNASSIGNED = "unassigned"
    BLOCKED    = "blocked"
    SPAM       = "spam"


@dataclass(frozen=True)
class NumberRule:
    """A single rule that can match one or more phone numbers."""
    id:          str
    region:      str
    match_type:  MatchType
    value:       str
    category:    MatchCategory
    description: str
    tags:        tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value.replace(" ", "").replace("-", "")
                           if self.match_type != MatchType.RANGE else self.value.strip())


@dataclass(frozen=True)
class ValidationResult:
    """Result returned by the validator for a single number."""
    number:        str
    is_blocked:    bool
    matched_rules: tuple[NumberRule, ...] = field(default_factory=tuple)
    reasons:       tuple[str, ...]        = field(default_factory=tuple)

    @property
    def primary_reason(self) -> Optional[str]:
        return self.reasons[0] if self.reasons else None

    @property
    def categories(self) -> set[MatchCategory]:
        return {r.category for r in self.matched_rules}

    def as_dict(self) -> dict:
        return {
            "number":     self.number,
            "is_blocked": self.is_blocked,
            "reasons":    list(self.reasons),
            "categories": [c.value for c in self.categories],
            "rules": [
                {
                    "id":          r.id,
                    "region":      r.region,
                    "match_type":  r.match_type.value,
                    "category":    r.category.value,
                    "description": r.description,
                }
                for r in self.matched_rules
            ],
        }
