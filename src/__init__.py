"""
Proportional Squad-Pay source package.
Exposes parser, calculator, and paypal_client modules.
"""

from src.calculator import calculate_shares, calculate_detailed_breakdown

try:
    from src.parser import parse_game_logs
except ImportError:
    parse_game_logs = None

try:
    from src.paypal_client import PayPalClient
except ImportError:
    PayPalClient = None

__all__ = [
    "parse_game_logs",
    "calculate_shares",
    "calculate_detailed_breakdown",
    "PayPalClient",
]
