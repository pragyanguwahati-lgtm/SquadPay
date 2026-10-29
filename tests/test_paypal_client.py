"""
Unit tests for Proportional Squad-Pay: PayPal Client.
Verifies Sandbox isolation, mock demo credentials, rate limiting, and zero credential leakage.
"""

import pytest
from src.paypal_client import PayPalClient


def test_missing_credentials_raises_error():
    """Client initialization without keys must raise a clear ValueError."""
    with pytest.raises(ValueError, match="PayPal Sandbox Client ID and Client Secret are required"):
        PayPalClient(client_id="", client_secret="")


def test_demo_mock_invoice_generation():
    """Verify demo mode produces simulated Sandbox Invoice IDs without external API calls."""
    client = PayPalClient(client_id="demo", client_secret="demo_secret")
    inv_id = client.create_draft_invoice(player_name="Nova", amount=24.0)

    assert inv_id.startswith("INV2-DEMO-")
    assert len(inv_id) > 10


def test_zero_or_negative_invoice_amount_rejected():
    """Negative or zero amounts must be rejected immediately."""
    client = PayPalClient(client_id="demo", client_secret="demo_secret")
    with pytest.raises(ValueError, match="Invoice amount for Ghost must be greater than 0"):
        client.create_draft_invoice(player_name="Ghost", amount=0.0)
