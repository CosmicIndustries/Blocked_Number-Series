"""
Blocked Number Series
~~~~~~~~~~~~~~~~~~~~~
    from blocked_numbers import Validator
    v = Validator()
    print(v.validate("+1 800 555 1234").is_blocked)  # True
"""

from .models    import MatchCategory, MatchType, NumberRule, ValidationResult
from .loader    import load_rules
from .validator import Validator, normalise

__all__ = [
    "Validator", "ValidationResult", "NumberRule",
    "MatchType", "MatchCategory", "load_rules", "normalise",
]
__version__ = "2.0.0"
