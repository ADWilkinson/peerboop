"""Regression checks for the calculation distributed in the Markdown skill.

The recipe runs only inside Grok's existing calculation tool. These tests load
that checked-in Python block directly; they do not create a second runtime.
"""

import re
import unittest
from fractions import Fraction
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/peerboop-p2p/SKILL.md"
USDC = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
POLICY_FLAGS = (
    "whitelistEnabled",
    "disputeProtectionOptedOut",
    "disputeProtectionRequiresStake",
    "sellerAutomatedReleaseAvailable",
    "sellerAutomatedReleaseEnabled",
)


def public_row(**changes):
    row = {
        "id": "revolut-public",
        "chainId": 8453,
        "token": USDC,
        "currency": "GBP",
        "paymentPlatform": "revolut",
        "feeBps": "95",
        "takerConversionRate": "1000000000000000000",
        "availableTokenAmount": "110770000",
        "intentAmountMin": "1000000",
        "intentAmountMax": "209078553",
        "conversionRate": "1000000000000000000",
        "spread": 0,
        "depositor": "0xAbC0000000000000000000000000000000000001",
        "rateManagerId": None,
        "successRate": 0,
        "fillCount": 0,
        **dict.fromkeys(POLICY_FLAGS, False),
    }
    row.update(changes)
    return row


class PublicPriceRecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blocks = re.findall(r"^```python\s*\n(.*?)^```\s*$", SKILL.read_text(), re.M | re.S)
        recipes = [block for block in blocks if re.search(r"^def rank_public_rows\(", block, re.M)]
        if len(recipes) != 1:
            raise AssertionError("expected one rank_public_rows Python recipe in the canonical skill")
        namespace = {}
        exec(compile(recipes[0], str(SKILL), "exec"), namespace)
        cls.rank = staticmethod(namespace["rank_public_rows"])
        cls.market_rate = staticmethod(namespace["market_rate"])
        cls.sell_snapshot = staticmethod(namespace["sell_snapshot"])

    def test_cheaper_eligible_revolut_beats_larger_wise_offer(self):
        revolut = public_row()
        wise = public_row(
            id="wise-large", paymentPlatform="wise", takerConversionRate="1020000000000000000",
            availableTokenAmount="900000000000", intentAmountMax="900000000000",
            successRate=100, fillCount=10000,
        )
        ranked = self.rank([wise, revolut], 100_000_000, "GBP", 10_000)
        self.assertEqual([item[1] for item in ranked], ["revolut", "wise"])
        self.assertEqual(ranked[0][:4], (10_096, "revolut", 959_111, 100_000_000))
        self.assertEqual(ranked[1][0], 10_298)
        self.assertIs(ranked[0][4], revolut)

    def test_net_amount_is_not_enough_gross_liquidity(self):
        cheap_short = public_row(
            id="too-small", takerConversionRate="500000000000000000", availableTokenAmount="100000000",
        )
        valid = public_row()
        self.assertEqual(self.rank([cheap_short, valid], 100_000_000, "GBP", 10_000)[0][4], valid)
        self.assertEqual(self.rank([cheap_short], 100_000_000, "GBP", 10_000), [])

    def test_gross_must_meet_offer_limits_and_available_balance(self):
        gross = "100959111"
        exact = public_row(intentAmountMin=gross, intentAmountMax=gross, availableTokenAmount=gross)
        self.assertEqual(len(self.rank([exact], 100_000_000, "GBP", 10_000)), 1)
        for changes in (
            {"availableTokenAmount": "100959110"},
            {"intentAmountMax": "100959110"},
            {"intentAmountMin": "100959112"},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(self.rank([public_row(**changes)], 100_000_000, "GBP", 10_000), [])

    def test_cheapest_offer_at_exact_gross_liquidity_boundary_is_not_skipped(self):
        cheapest = public_row(
            availableTokenAmount="100959111", intentAmountMax="100959111",
        )
        fallback = public_row(
            id="wise-fallback", paymentPlatform="wise", takerConversionRate="1020000000000000000",
        )
        ranked = self.rank([fallback, cheapest], 100_000_000, "GBP", 10_000)
        self.assertEqual([item[1] for item in ranked], ["revolut", "wise"])
        self.assertIs(ranked[0][4], cheapest)
        self.assertEqual(ranked[0][:4], (10_096, "revolut", 959_111, 100_000_000))

    def test_whitelisted_rows_without_stake_are_excluded(self):
        self.assertEqual(self.rank([public_row(whitelistEnabled=True)], 100_000_000, "GBP", 10_000), [])

    def test_stake_backed_rows_are_public_even_when_whitelisted(self):
        row = public_row(whitelistEnabled=True, disputeProtectionRequiresStake=True)
        ranked = self.rank([row], 100_000_000, "GBP", 10_000)
        self.assertEqual(len(ranked), 1)
        self.assertIs(ranked[0][4], row)

    def test_equal_price_prefers_offer_without_stake(self):
        staked = public_row(id="staked", paymentPlatform="aaa", disputeProtectionRequiresStake=True)
        open_offer = public_row(id="open", paymentPlatform="zzz")
        ranked = self.rank([staked, open_offer], 100_000_000, "GBP", 10_000)
        self.assertIs(ranked[0][4], open_offer)

    def test_invalid_or_unknown_policy_flags_are_excluded(self):
        contradictory = public_row(disputeProtectionOptedOut=True, disputeProtectionRequiresStake=True)
        self.assertEqual(self.rank([contradictory], 100_000_000, "GBP", 10_000), [])
        for flag in POLICY_FLAGS:
            for value in (None, "false"):
                with self.subTest(flag=flag, value=value):
                    self.assertEqual(self.rank([public_row(**{flag: value})], 100_000_000, "GBP", 10_000), [])
            missing = public_row()
            del missing[flag]
            with self.subTest(flag=flag, missing=True):
                self.assertEqual(self.rank([missing], 100_000_000, "GBP", 10_000), [])
        for flag in ("sellerAutomatedReleaseAvailable", "sellerAutomatedReleaseEnabled"):
            with self.subTest(flag=flag):
                self.assertEqual(self.rank([public_row(**{flag: True})], 100_000_000, "GBP", 10_000), [])

    def test_rate_managed_rows_are_ordinary_offers(self):
        managed = public_row(rateManagerId="0x1111111111111111111111111111111111111111")
        self.assertEqual(len(self.rank([managed], 100_000_000, "GBP", 10_000)), 1)

    def test_market_rate_is_median_implied_oracle_rate(self):
        rows = [
            public_row(takerConversionRate="954395146475010900", spread=6.5),
            public_row(takerConversionRate="976798788411044100", spread=9),
            public_row(takerConversionRate="1229691098584985800", spread=37.22),
            public_row(currency="USD", takerConversionRate="2000000000000000000", spread=0),
            public_row(spread=None),
        ]
        rate = self.market_rate(rows, "GBP")
        self.assertAlmostEqual(float(rate), 0.89614, places=4)
        self.assertIsNone(self.market_rate([public_row(spread=None)], "GBP"))

    def test_sell_snapshot_reports_market_value_and_public_competition(self):
        rows = [
            public_row(conversionRate="954395146475010900", takerConversionRate="954395146475010900", spread=6.5, availableTokenAmount="3192711160",
                       depositor="0x0000000000000000000000000000000000000001"),
            public_row(conversionRate="976798788411044100", takerConversionRate="976798788411044100", spread=9, availableTokenAmount="612552073",
                       depositor="0x0000000000000000000000000000000000000002"),
            public_row(conversionRate="900000000000000000", takerConversionRate="900000000000000000", spread=0.4, whitelistEnabled=True,
                       depositor="0x0000000000000000000000000000000000000003"),
            public_row(paymentPlatform="wise", conversionRate="800000000000000000", takerConversionRate="800000000000000000", spread=-10,
                       depositor="0x0000000000000000000000000000000000000004"),
        ]
        snap = self.sell_snapshot(rows, "revolut", "GBP", 250_000_000, 10_000)
        self.assertEqual(snap["sellers"], 2)
        self.assertEqual(snap["listed_micro"], 3_805_263_233)
        self.assertAlmostEqual(snap["lowest_premium_pct"], 6.5, places=1)
        self.assertAlmostEqual(float(snap["lowest"]), 0.954395, places=6)
        self.assertTrue(22_390 <= snap["market_minor"] <= 22_410)

    def test_rate_managed_rows_use_the_taker_rate(self):
        managed = public_row(rateManagerId="0x1111111111111111111111111111111111111111",
                             conversionRate="903183000000000000", takerConversionRate="904087000000000000", spread=0.886)
        plain = public_row(conversionRate="896147000000000000", takerConversionRate="896147000000000000", spread=0,
                           paymentPlatform="wise")
        self.assertAlmostEqual(float(self.market_rate([managed, plain], "GBP")), 0.896147, places=5)
        snap = self.sell_snapshot([managed, plain], "revolut", "GBP", 100_000_000, 10_000)
        self.assertEqual(snap["lowest"], Fraction(904087, 1_000_000))
        self.assertEqual(snap["lowest_premium_pct"], 0.9)

    def test_null_spread_rows_still_compete_with_computed_premium(self):
        rows = [public_row(paymentPlatform="wise", spread=0),
                public_row(takerConversionRate="1020000000000000000", spread=None)]
        snap = self.sell_snapshot(rows, "revolut", "GBP", 100_000_000, 10_000)
        self.assertEqual(snap["lowest_premium_pct"], 2.0)
        self.assertIsNone(self.sell_snapshot([public_row(spread=None)], "revolut", "GBP", 1, 10_000)["lowest_premium_pct"])

    def test_sell_snapshot_without_offers_keeps_market_value(self):
        rows = [public_row(paymentPlatform="wise", spread=0)]
        snap = self.sell_snapshot(rows, "revolut", "GBP", 100_000_000, 10_000)
        self.assertIsNone(snap["lowest"])
        self.assertEqual(snap["market_minor"], 10_000)

    def test_other_chain_token_or_currency_is_excluded(self):
        for changes in (
            {"chainId": 1}, {"token": "0x0000000000000000000000000000000000000000"}, {"currency": "USD"},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(self.rank([public_row(**changes)], 100_000_000, "GBP", 10_000), [])

    def test_zero_negative_or_invalid_price_inputs_are_excluded(self):
        for target in (0, -1):
            self.assertEqual(self.rank([public_row()], target, "GBP", 10_000), [])
        for changes in ({"feeBps": "-1"}, {"feeBps": "10000"}, {"takerConversionRate": "0"}, {"takerConversionRate": "-1"}):
            with self.subTest(changes=changes):
                self.assertEqual(self.rank([public_row(**changes)], 100_000_000, "GBP", 10_000), [])

    def test_zero_fee_preserves_exact_net(self):
        result = self.rank([public_row(feeBps="0")], 100_000_000, "GBP", 10_000)[0]
        self.assertEqual(result[:4], (10_000, "revolut", 0, 100_000_000))

    def test_explicit_currency_minor_units(self):
        yen = public_row(currency="JPY", takerConversionRate="150000000000000000000")
        dinar = public_row(currency="KWD", takerConversionRate="300000000000000000")
        self.assertEqual(self.rank([yen], 100_000_000, "JPY", 1_000_000)[0][0], 15_144)
        self.assertEqual(self.rank([dinar], 100_000_000, "KWD", 1_000)[0][0], 30_288)

    def test_all_valid_nonzero_fees_use_minimal_gross_without_rounding_payment_down(self):
        rate = 1_150_000_000_000_000_001
        for fee_bps in range(1, 10_000):
            for target in (1, 3, 9_999):
                row = public_row(
                    feeBps=str(fee_bps), takerConversionRate=str(rate), intentAmountMin="1",
                    intentAmountMax="1000000000000000000", availableTokenAmount="1000000000000000000",
                )
                ranked = self.rank([row], target, "GBP", 10_000)
                self.assertEqual(len(ranked), 1, (fee_bps, target))
                paid_minor, _, fee, net, _ = ranked[0]
                gross = net + fee
                self.assertEqual(net, target, (fee_bps, target))
                previous_gross = gross - 1
                previous_net = previous_gross - previous_gross * fee_bps // 10_000
                self.assertLess(previous_net, target, (fee_bps, target))
                self.assertLessEqual(fee * 10_000, gross * fee_bps)
                self.assertLess(gross * fee_bps, (fee + 1) * 10_000)
                self.assertGreaterEqual(paid_minor * 10_000 * 10**18, gross * rate)
                self.assertLess((paid_minor - 1) * 10_000 * 10**18, gross * rate)


if __name__ == "__main__":
    unittest.main()
