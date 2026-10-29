"""
Proportional Squad-Pay: Streamlit Application
PayPal AI Hackathon 2026

Ingests raw game server logs, parses player active hours using local Ollama (qwen2.5-coder:7b),
calculates proportional hosting splits, and generates PayPal Sandbox Invoice Drafts.
"""

import io
import os
import time
from typing import Dict, List, Optional

import streamlit as st
import pandas as pd

from src.parser import parse_game_logs, fallback_parse_game_logs
from src.calculator import calculate_shares, calculate_detailed_breakdown
from src.paypal_client import PayPalClient

# Configure page layout and metadata
st.set_page_config(
    page_title="SquadPay — Proportional Squad-Pay",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Cyberpunk / Fintech Dark Theme CSS adhering to design.md
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, .squad-title {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.05em;
    }

    /* Background accentuation */
    .stApp {
        background: radial-gradient(circle at 80% 20%, #15325b 0%, #081a2e 45%, #05101c 100%);
        color: #f3f7ff;
    }

    /* Custom Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(17, 38, 75, 0.7) 0%, rgba(7, 27, 26, 0.8) 100%);
        border: 1px solid rgba(72, 213, 165, 0.25);
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(72, 213, 165, 0.15);
        border: 1px solid #48d5a5;
        color: #48d5a5;
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-heading {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }

    .hero-subheading {
        color: #a5beb7;
        font-size: 15px;
        margin: 0;
        line-height: 1.5;
    }

    /* Stats Card Grid */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }

    .squad-card {
        background: rgba(17, 38, 75, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px 20px;
        transition: all 0.2s ease;
    }

    .squad-card:hover {
        border-color: #48d5a5;
        transform: translateY(-2px);
    }

    .card-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #a5beb7;
        margin-bottom: 6px;
    }

    .card-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #48d5a5;
    }

    /* Success Invoice Box */
    .invoice-box {
        background: rgba(8, 102, 237, 0.1);
        border: 1px solid #0866ed;
        border-radius: 10px;
        padding: 18px 24px;
        margin-top: 20px;
    }

    .invoice-tag {
        font-family: 'Courier New', Courier, monospace;
        background: #081a2e;
        border: 1px solid #48d5a5;
        color: #48d5a5;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_sidebar():
    """
    Renders sidebar for secure credentials entry and environment parameters.
    Adheres strictly to threat vectors 3, 4, 11, and 25 (Ephemeral session state).
    """
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-family: 'Orbitron'; font-size: 22px; font-weight: 800; color: #48d5a5;">SQUADPAY</span>
            <div style="font-size: 11px; color: #a5beb7;">CO-OP FINANCE ENGINE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("### 🔒 Secure Credentials")
    st.sidebar.caption(
        "API keys are held ephemerally in RAM (`st.session_state`) and never logged or written to disk."
    )

    # Initialize session keys if not set
    if "paypal_client_id" not in st.session_state:
        st.session_state["paypal_client_id"] = ""
    if "paypal_client_secret" not in st.session_state:
        st.session_state["paypal_client_secret"] = ""

    client_id_val = st.sidebar.text_input(
        "PayPal Sandbox Client ID",
        type="password",
        value=st.session_state["paypal_client_id"],
        placeholder="Enter Sandbox Client ID...",
        help="Obtain this from your PayPal Developer Dashboard (Sandbox App).",
    )
    st.session_state["paypal_client_id"] = client_id_val

    client_secret_val = st.sidebar.text_input(
        "PayPal Sandbox Client Secret",
        type="password",
        value=st.session_state["paypal_client_secret"],
        placeholder="Enter Sandbox Client Secret...",
        help="Your secret key is scrubbed in error outputs and never logged.",
    )
    st.session_state["paypal_client_secret"] = client_secret_val

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧠 AI Model Configuration")
    ai_model = st.sidebar.selectbox(
        "Ollama LLM Model",
        options=["qwen2.5-coder:7b", "llama3.2:latest", "mistral:latest"],
        index=0,
        help="Local AI execution protects gamer privacy by keeping logs offline.",
    )

    st.sidebar.markdown("---")
    # Quick demo credentials shortcut for hackathon judges
    st.sidebar.markdown("### ⚡ Hackathon Quick Test")
    if st.sidebar.button("Fill Demo Sandbox Keys", use_container_width=True):
        st.session_state["paypal_client_id"] = "demo"
        st.session_state["paypal_client_secret"] = "demo_secret"
        st.sidebar.success("Loaded demo Sandbox credentials for rapid evaluation!")
        st.rerun()

    st.sidebar.caption("PayPal AI Hackathon 2026 • Local-First Architecture")
    return ai_model


def main():
    ai_model = render_sidebar()

    # Top Hero Header
    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Level 03: Proportional Financial Settlement</span>
            <h1 class="hero-heading">Proportional Squad-Pay</h1>
            <p class="hero-subheading">
                Transform raw game server logs into fair, playtime-weighted splits.
                Calculated privately via <strong>local AI (Ollama)</strong> and routed to <strong>PayPal Sandbox Invoicing</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 1. Quest Parameters & Log Upload")
        total_cost = st.number_input(
            "Total Monthly Server Bill ($ USD)",
            min_value=1.0,
            max_value=10000.0,
            value=45.0,
            step=1.0,
            help="The total hosting cost to split among active players.",
        )

        # Threat Vector 16: Restrict file upload strictly to .txt and .log
        uploaded_file = st.file_uploader(
            "Upload Game Server Log (.txt, .log)",
            type=["txt", "log"],
            help="Minecraft, Palworld, Rust, or custom game server logs with join/leave events.",
        )

        # Convenient sample log loader for judges
        use_sample = st.checkbox("Or use bundled hackathon `sample_log.txt` (Instant Test)", value=False)

        raw_log_content: Optional[str] = None

        if uploaded_file is not None:
            # Threat Vector 21 & 22: Read strictly into RAM (BytesIO), never write to disk
            raw_log_content = uploaded_file.getvalue().decode("utf-8", errors="replace")
            st.success(f"Loaded uploaded log ({len(raw_log_content.splitlines())} lines).")
        elif use_sample:
            sample_path = os.path.join(os.path.dirname(__file__), "sample_log.txt")
            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    raw_log_content = f.read()
                st.info("Loaded bundled `sample_log.txt` (15 lines).")
            else:
                st.warning("sample_log.txt not found in project root.")

        if raw_log_content:
            with st.expander("📄 View Raw Log Preview (First 10 lines)", expanded=False):
                preview_lines = "\n".join(raw_log_content.splitlines()[:10])
                st.code(preview_lines, language="text")

    with col2:
        st.markdown("### 2. Execution Pipeline")
        st.markdown(
            """
            Click below to execute the 3-stage sequence:
            1. **Local Ollama Agent** extracts player playtime into strict JSON.
            2. **Financial Engine** applies proportional cost splitting and penny reconciliation.
            3. **PayPal Sandbox** generates individual draft invoices.
            """
        )

        can_proceed = bool(raw_log_content)
        start_btn = st.button(
            "🚀 Execute Squad-Pay Quest",
            type="primary",
            disabled=not can_proceed,
            use_container_width=True,
        )

        if not can_proceed:
            st.caption("👈 Upload a server log or check 'use bundled sample' to begin.")

    # Processing & Results Section
    if start_btn and raw_log_content:
        st.markdown("---")
        st.markdown("### 3. Pipeline Execution Results")

        # Step 1: AI Parsing
        with st.status("Analyzing server log with local AI agent...", expanded=True) as status:
            st.write(f"Initiating Ollama prompt on model `{ai_model}`...")
            playtime_map: Dict[str, float] = {}
            try:
                playtime_map = parse_game_logs(raw_log_content, model=ai_model)
                st.write(f"Successfully extracted {len(playtime_map)} players from log.")
            except ConnectionError as ce:
                st.warning(
                    f"🔌 Local Ollama runtime offline: {str(ce)}\n\n"
                    "⚡ Switched to offline deterministic timestamp parser so you can evaluate the entire pipeline."
                )
                playtime_map = fallback_parse_game_logs(raw_log_content)
                st.write(f"Offline parser extracted {len(playtime_map)} players: {playtime_map}")
            except Exception as e:
                status.update(label="Log parsing error", state="error")
                st.error(f"❌ Error during AI parsing: {str(e)}")
                return

            # Step 2: Proportional Calculation
            st.write("Calculating proportional shares with exact penny reconciliation...")
            try:
                shares = calculate_shares(playtime_map, total_cost)
                detailed_records = calculate_detailed_breakdown(playtime_map, total_cost)
            except Exception as e:
                status.update(label="Calculation error", state="error")
                st.error(f"❌ Calculation failed: {str(e)}")
                return

            # Step 3: PayPal Invoicing Execution
            st.write("Authenticating with PayPal REST SDK (Sandbox Mode)...")
            invoice_results = {}
            try:
                paypal = PayPalClient()
            except ValueError as ve:
                status.update(label="Missing PayPal Credentials", state="error")
                st.error(f"🔑 {str(ve)}")
                st.info("Tip: Click 'Fill Demo Sandbox Keys' in the sidebar for rapid judge evaluation.")
                return

            st.write(f"Generating Sandbox Invoice drafts for {len(shares)} players...")
            progress_bar = st.progress(0.0)

            for idx, (player, amount) in enumerate(shares.items()):
                try:
                    inv_id = paypal.create_draft_invoice(
                        player_name=player,
                        amount=amount,
                        server_name="Squad Server",
                    )
                    invoice_results[player] = inv_id
                except Exception as pe:
                    st.warning(f"Could not create invoice for {player}: {pe}")
                    invoice_results[player] = "FAILED"
                progress_bar.progress((idx + 1) / len(shares))

            status.update(label="Quest Completed Successfully!", state="complete")

        # Display Top Summary Metrics
        st.markdown("#### 📊 Squad Playtime & Cost Breakdown")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        total_hours = sum(playtime_map.values())
        with m_col1:
            st.metric("Total Server Bill", f"${total_cost:.2f}")
        with m_col2:
            st.metric("Active Players", len(playtime_map))
        with m_col3:
            st.metric("Total Playtime", f"{total_hours:.1f} hrs")
        with m_col4:
            st.metric("Invoices Created", len(invoice_results))

        # Render Data Table
        table_data = []
        for rec in detailed_records:
            player = rec["player_name"]
            table_data.append({
                "Player Name": player,
                "Hours Played": rec["hours_played"],
                "% of Total": rec["percentage"],
                "Amount Owed": rec["formatted_amount"],
                "PayPal Sandbox Invoice ID": invoice_results.get(player, "N/A"),
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Success Banner with Final Invoice IDs
        st.markdown(
            """
            <div class="invoice-box">
                <h3 style="color: #48d5a5; margin-top: 0;">🎉 PayPal Sandbox Invoices Generated!</h3>
                <p style="color: #f3f7ff; margin-bottom: 12px;">
                    All proportional drafts have been successfully created via the PayPal REST API:
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for player, inv_id in invoice_results.items():
            amt = shares.get(player, 0.0)
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.markdown(f"**{player}** (Amount: `${amt:.2f}`)")
            with col_b:
                if inv_id != "FAILED":
                    st.code(inv_id, language="text")
                else:
                    st.error("Draft generation failed")


if __name__ == "__main__":
    main()
