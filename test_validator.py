"""
Tests for Blocked Number Series v2
"""

import json
import pytest
from pathlib import Path

from blocked_numbers import Validator, normalise
from blocked_numbers.models import MatchCategory


@pytest.fixture(scope="module")
def validator():
    return Validator()


@pytest.fixture(scope="module")
def sample_data():
    path = Path(__file__).parent.parent / "data" / "sample_numbers.json"
    with path.open() as fh:
        return json.load(fh)["samples"]


class TestNormalise:
    def test_strips_dashes(self):
        assert normalise("1-800-555-1234") == "18005551234"
    def test_strips_spaces(self):
        assert normalise("1 800 555 1234") == "18005551234"
    def test_strips_parens(self):
        assert normalise("(800) 555-1234") == "8005551234"
    def test_strips_plus(self):
        assert normalise("+1 800 555 1234") == "18005551234"
    def test_strips_dots(self):
        assert normalise("1.800.555.1234") == "18005551234"
    def test_passthrough(self):
        assert normalise("18005551234") == "18005551234"
    def test_short(self):
        assert normalise("911") == "911"


class TestPrefix:
    def test_us_800(self, validator):
        r = validator.validate("18005551234")
        assert r.is_blocked
        assert MatchCategory.TOLL_FREE in r.categories
    def test_us_888(self, validator):
        assert validator.is_blocked("18885551234")
    def test_us_833(self, validator):
        assert validator.is_blocked("18335551234")
    def test_us_844(self, validator):
        assert validator.is_blocked("18445551234")
    def test_us_855(self, validator):
        assert validator.is_blocked("18555551234")
    def test_us_866(self, validator):
        assert validator.is_blocked("18665551234")
    def test_us_877(self, validator):
        assert validator.is_blocked("18775551234")
    def test_us_900_premium(self, validator):
        r = validator.validate("19005551234")
        assert r.is_blocked
        assert MatchCategory.PREMIUM in r.categories
    def test_us_555_reserved(self, validator):
        r = validator.validate("15554567890")
        assert r.is_blocked
        assert MatchCategory.RESERVED in r.categories
    def test_uk_0800(self, validator):
        assert validator.is_blocked("08001234567")
    def test_uk_premium_09(self, validator):
        assert validator.is_blocked("09012345678")
    def test_ru_8800(self, validator):
        assert validator.is_blocked("88001234567")
    def test_jp_0120(self, validator):
        assert validator.is_blocked("01201234567")


class TestExact:
    def test_us_911(self, validator):
        r = validator.validate("911")
        assert r.is_blocked
        assert MatchCategory.EMERGENCY in r.categories
    def test_us_988(self, validator):
        assert validator.is_blocked("988")
    def test_us_411(self, validator):
        assert validator.is_blocked("411")
    def test_global_112(self, validator):
        assert validator.is_blocked("112")
    def test_uk_999(self, validator):
        assert validator.is_blocked("999")
    def test_au_000(self, validator):
        assert validator.is_blocked("000")
    def test_nz_111(self, validator):
        assert validator.is_blocked("111")
    def test_fr_15(self, validator):
        assert validator.is_blocked("15")
    def test_fr_17(self, validator):
        assert validator.is_blocked("17")
    def test_in_100(self, validator):
        assert validator.is_blocked("100")
    def test_za_10111(self, validator):
        assert validator.is_blocked("10111")
    def test_jp_119(self, validator):
        assert validator.is_blocked("119")
    def test_br_190(self, validator):
        assert validator.is_blocked("190")


class TestSuffix:
    def test_0000_spam(self, validator):
        r = validator.validate("12125550000")
        assert r.is_blocked
        assert MatchCategory.SPAM in r.categories
    def test_no_false_positive(self, validator):
        r = validator.validate("12025551234")
        spam = [x for x in r.matched_rules if x.category == MatchCategory.SPAM]
        assert not spam


class TestRange:
    def test_itu_700(self, validator):
        r = validator.validate("700123456")
        assert r.is_blocked
        assert MatchCategory.RESERVED in r.categories
    def test_itu_799(self, validator):
        assert validator.is_blocked("799999999")
    def test_itu_below_boundary(self, validator):
        r = validator.validate("699123456")
        reserved = [x for x in r.matched_rules if x.id == "GLOBAL-ITU-RES"]
        assert not reserved
    def test_eu_116000(self, validator):
        assert validator.is_blocked("116000")
    def test_eu_116999(self, validator):
        assert validator.is_blocked("116999")
    def test_eu_116_mid(self, validator):
        assert validator.is_blocked("116500")


class TestClean:
    def test_us_landline(self, validator):
        assert not validator.is_blocked("12025551234")
    def test_uk_mobile(self, validator):
        assert not validator.is_blocked("447911123456")
    def test_au_mobile(self, validator):
        assert not validator.is_blocked("61412345678")
    def test_de_mobile(self, validator):
        assert not validator.is_blocked("4915123456789")


class TestBatch:
    def test_count_preserved(self, validator):
        results = validator.validate_batch(["911", "12025551234", "18005551234"])
        assert len(results) == 3
    def test_order_preserved(self, validator):
        results = validator.validate_batch(["12025551234", "911", "18005551234"])
        assert not results[0].is_blocked
        assert results[1].is_blocked
        assert results[2].is_blocked


class TestRegionFilter:
    def test_global_always_applies(self):
        v = Validator(regions=["US"])
        assert v.is_blocked("112")
    def test_foreign_prefix_excluded(self):
        v = Validator(regions=["US"])
        r = v.validate("08001234567")
        gb_rules = [x for x in r.matched_rules if x.region == "GB"]
        assert not gb_rules


class TestResultObject:
    def test_dict_keys(self, validator):
        d = validator.validate("18005551234").as_dict()
        assert all(k in d for k in ("number","is_blocked","reasons","categories","rules"))
    def test_primary_reason_none_when_clear(self, validator):
        assert validator.validate("12025551234").primary_reason is None
    def test_primary_reason_set_when_blocked(self, validator):
        assert validator.validate("18005551234").primary_reason is not None
    def test_invalid_raises(self, validator):
        with pytest.raises(ValueError):
            validator.validate("not-a-number")


class TestSampleRegression:
    def test_all_samples(self, validator, sample_data):
        failures = []
        for s in sample_data:
            r = validator.validate(s["number"])
            if r.is_blocked != s["expected_blocked"]:
                failures.append(
                    f"{s['number']!r} ({s['note']}): "
                    f"expected={s['expected_blocked']}, got={r.is_blocked}"
                )
        assert not failures, "\n".join(failures)
