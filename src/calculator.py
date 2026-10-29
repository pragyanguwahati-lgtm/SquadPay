"""
Financial calculation module for Proportional Squad-Pay.
Calculates proportional monetary shares from playtime hours and total server cost.
Enforces strict 2-decimal financial rounding and exact penny reconciliation.
"""

import json
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Union


def calculate_shares(
    playtime_data: Union[Dict[str, float], str],
    total_cost: float,
) -> Dict[str, float]:
    """
    Takes player playtime mapping and total server cost, returning a dictionary of
    calculated monetary shares formatted to two decimal places.

    Args:
        playtime_data: Dict mapping player names to hours, or JSON string of the same.
        total_cost: Total monthly server hosting bill in currency units (e.g. 45.00).

    Returns:
        Dict[str, float]: Mapping of player_name to calculated share, e.g. {"Nova": 22.50, "Ghost": 15.00}

    Raises:
        ValueError: If total_cost is negative or playtime_data is invalid.
    """
    if total_cost < 0:
        raise ValueError("Total server cost cannot be negative.")

    # Parse JSON string if passed as string
    if isinstance(playtime_data, str):
        try:
            playtime_dict = json.loads(playtime_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string provided for playtime data: {e}") from e
    elif isinstance(playtime_data, dict):
        playtime_dict = playtime_data
    else:
        raise ValueError("playtime_data must be a dict or a valid JSON string.")

    if not playtime_dict:
        return {}

    # Extract valid positive hours
    sanitized: Dict[str, Decimal] = {}
    for player, hours in playtime_dict.items():
        try:
            h = Decimal(str(hours))
            if h < 0:
                h = Decimal("0")
            sanitized[str(player).strip()] = h
        except Exception:
            continue

    if not sanitized:
        return {}

    total_hours = sum(sanitized.values())
    cost_dec = Decimal(str(round(total_cost, 2)))

    # If all hours are zero, split equally among all players
    if total_hours == 0:
        num_players = Decimal(len(sanitized))
        equal_share = (cost_dec / num_players).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        result = {p: float(equal_share) for p in sanitized}
        _reconcile_penny_difference(result, float(cost_dec))
        return result

    # Proportional calculation with 2 decimal precision
    calculated_shares: Dict[str, float] = {}
    for player, hours in sanitized.items():
        share = (hours / total_hours) * cost_dec
        rounded_share = share.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        calculated_shares[player] = float(rounded_share)

    # Reconcile penny difference to ensure sum(shares) == total_cost exactly
    _reconcile_penny_difference(calculated_shares, float(cost_dec))

    return calculated_shares


def calculate_detailed_breakdown(
    playtime_data: Union[Dict[str, float], str],
    total_cost: float,
) -> List[Dict[str, Any]]:
    """
    Produces tabular records for UI presentation:
    Player Name | Hours Played | % of Total | Amount Owed
    """
    shares = calculate_shares(playtime_data, total_cost)
    if isinstance(playtime_data, str):
        raw_dict = json.loads(playtime_data)
    else:
        raw_dict = playtime_data or {}

    total_hours = sum(float(raw_dict.get(p, 0)) for p in shares)

    records = []
    for player, amount in shares.items():
        hours = float(raw_dict.get(player, 0.0))
        percentage = (hours / total_hours * 100.0) if total_hours > 0 else (100.0 / len(shares))
        records.append({
            "player_name": player,
            "hours_played": round(hours, 2),
            "percentage": f"{percentage:.1f}%",
            "amount_owed": amount,
            "formatted_amount": f"${amount:.2f}",
        })
    return records


def _reconcile_penny_difference(shares: Dict[str, float], total_cost: float) -> None:
    """
    Adjusts the largest share by the remaining penny difference so sum(shares) == total_cost.
    """
    if not shares:
        return
    current_sum = round(sum(shares.values()), 2)
    diff = round(total_cost - current_sum, 2)
    if abs(diff) > 0.0001:
        # Find player with largest share to absorb the penny adjustment
        target_player = max(shares, key=lambda k: shares[k])
        shares[target_player] = round(shares[target_player] + diff, 2)
