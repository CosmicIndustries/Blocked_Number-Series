"""
Blocked Number Series — Data Loader
"""
from __future__ import annotations

import json
import re
import logging
from pathlib import Path
from typing import Iterator

from .models import MatchCategory, MatchType, NumberRule

log = logging.getLogger(__name__)

_DEFAULT_DATA = Path(__file__).parent.parent / "data" / "blocked_numbers.json"

_MATCH_TYPE_MAP: dict[str, MatchType] = {
    "prefix":   MatchType.PREFIX,
    "suffix":   MatchType.SUFFIX,
    "contains": MatchType.CONTAINS,
    "exact":    MatchType.EXACT,
    "range":    MatchType.RANGE,
    "pattern":  MatchType.PATTERN,
}
_CATEGORY_MAP: dict[str, MatchCategory] = {
    "toll_free":  MatchCategory.TOLL_FREE,
    "emergency":  MatchCategory.EMERGENCY,
    "reserved":   MatchCategory.RESERVED,
    "premium":    MatchCategory.PREMIUM,
    "special":    MatchCategory.SPECIAL,
    "unassigned": MatchCategory.UNASSIGNED,
    "blocked":    MatchCategory.BLOCKED,
    "spam":       MatchCategory.SPAM,
}


def _iter_rules(raw: dict) -> Iterator[NumberRule]:
    for entry in raw.get("rules", []):
        try:
            yield NumberRule(
                id=entry["id"],
                region=entry.get("region", "GLOBAL").upper(),
                match_type=_MATCH_TYPE_MAP[entry["match_type"]],
                value=entry["value"],
                category=_CATEGORY_MAP[entry["category"]],
                description=entry.get("description", ""),
                tags=tuple(entry.get("tags", [])),
            )
        except (KeyError, TypeError) as exc:
            log.warning("Skipping malformed rule %r: %s", entry.get("id"), exc)


def load_rules(path: Path | str | None = None) -> list[NumberRule]:
    target = Path(path) if path else _DEFAULT_DATA
    if not target.exists():
        raise FileNotFoundError(f"Data file not found: {target}")
    with target.open(encoding="utf-8") as fh:
        raw = json.load(fh)
    rules = list(_iter_rules(raw))
    log.debug("Loaded %d rules from %s", len(rules), target)
    return rules


def compile_pattern(rule: NumberRule) -> re.Pattern | None:
    v = re.escape(rule.value)
    match rule.match_type:
        case MatchType.PREFIX:
            return re.compile(rf"^{v}")
        case MatchType.SUFFIX:
            return re.compile(rf"{v}$")
        case MatchType.CONTAINS:
            return re.compile(v)
        case MatchType.EXACT:
            return re.compile(rf"^{v}$")
        case MatchType.PATTERN:
            pat = re.escape(rule.value).replace(r"\X", r"\d")
            return re.compile(pat)
        case MatchType.RANGE:
            return None
        case _:
            return None
