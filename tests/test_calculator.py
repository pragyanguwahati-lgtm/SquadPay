"""
Unit tests for Proportional Squad-Pay: Proportional Cost Calculator.
Verifies exact penny reconciliation, fractional rounding, zero-hour safety, and edge cases.
"""

import pytest
from src.calculator import calculate_shares, calculate_detailed_breakdown


def test_standard_unequal_split():
    """Verify 40/30/20/10 proportional split with $60 bill."""
    playtime = {"Nova": 48.0, "Ghost": 36.0, "Pixel": 24.0, "Moss": 12.0}
    total_bill = 60.0
    shares = calculate_shares(playtime, total_bill)

    assert shares["Nova"] == 24.0
    assert shares["Ghost"] == 18.0
    assert shares["Pixel"] == 12.0
    assert shares["Moss"] == 6.0
    assert round(sum(shares.values()), 2) == 60.0


def test_exact_penny_reconciliation_repeating_fractions():
    """
    Verify exact penny reconciliation for 3 players splitting $100 ($33.333...).
    The sum must equal $100.00 exactly without losing or gaining a cent.
    """
    playtime = {"Player1": 10.0, "Player2": 10.0, "Player3": 10.0}
    total_bill = 100.0
    shares = calculate_shares(playtime, total_bill)

    total_shares = round(sum(shares.values()), 2)
    assert total_shares == 100.0
    # One player receives the extra 1 cent discrepancy
    assert shares["Player1"] in (33.33, 33.34)
    assert shares["Player2"] in (33.33, 33.34)
    assert shares["Player3"] in (33.33, 33.34)


def test_single_player_pays_full_bill():
    """If only one player logged hours, they bear 100% of the cost."""
    playtime = {"SoloGamer": 55.5}
    total_bill = 45.0
    shares = calculate_shares(playtime, total_bill)

    assert shares["SoloGamer"] == 45.0
    assert sum(shares.values()) == 45.0


def test_zero_total_hours_splits_equally():
    """If all active hours are zero, server cost is divided equally among members."""
    playtime = {"Ghost": 0.0, "Pixel": 0.0}
    shares = calculate_shares(playtime, 50.0)
    assert shares["Ghost"] == 25.0
    assert shares["Pixel"] == 25.0
    assert sum(shares.values()) == 50.0


def test_empty_playtime_returns_empty_dict():
    """Empty player dictionary safely returns empty result."""
    shares = calculate_shares({}, 50.0)
    assert shares == {}


def test_negative_cost_raises_error():
    """Negative total cost must raise ValueError safely."""
    playtime = {"Nova": 10.0}
    with pytest.raises(ValueError, match="Total server cost cannot be negative"):
        calculate_shares(playtime, -20.0)


def test_detailed_breakdown_structure():
    """Verify calculate_detailed_breakdown outputs structured audit metadata."""
    playtime = {"Nova": 40.0, "Ghost": 60.0}
    total_bill = 50.0
    breakdown = calculate_detailed_breakdown(playtime, total_bill)

    assert len(breakdown) == 2
    ghost_record = next(r for r in breakdown if r["player_name"] == "Ghost")
    assert ghost_record["hours_played"] == 60.0
    assert ghost_record["percentage"] == "60.0%"
    assert ghost_record["amount_owed"] == 30.0
    assert ghost_record["formatted_amount"] == "$30.00"
