# 🎮 SquadPay — Co-Op Server Bill Splitting

> **Turn multiplayer game server logs into fair, playtime-proportional payment requests powered by AI (Google Gemini & Local Ollama) and PayPal.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![PayPal REST API](https://img.shields.io/badge/PayPal-Sandbox%20REST%20v2-00457C.svg)](https://developer.paypal.com)
[![Google Gemini API](https://img.shields.io/badge/Gemini-2.5--flash%20%26%203.7--flash-8E75C2.svg)](https://ai.google.dev)

---

## 📖 Table of Contents

- [Overview & The Problem](#-overview--the-problem)
- [How SquadPay Works](#-how-squadpay-works)
- [Architecture & Key Components](#-architecture--key-components)
- [AI Parsing Engines](#-ai-parsing-engines)
- [Financial Calculation & Penny Reconciliation](#-financial-calculation--penny-reconciliation)
- [PayPal Sandbox Integration](#-paypal-sandbox-integration)
- [Quickstart Guide](#-quickstart-guide)
- [Configuration & Secrets](#-configuration--secrets)
- [Running Automated Tests](#-running-automated-tests)
- [Security & Privacy Architecture](#-security--privacy-architecture)
- [Project Directory Layout](#-project-directory-layout)
- [Contributing & License](#-contributing--license)

---

## 🌟 Overview & The Problem

Multiplayer gaming squads (Minecraft, Palworld, Rust, ARK, Valheim) frequently host dedicated servers. At the end of each billing cycle, server admins face recurring friction:
- **Flat splits are unfair:** A squad member who logged 2 hours pays the exact same amount as someone who logged 50 hours.
- **Manual log auditing is tedious:** Server admins must manually inspect thousands of lines of console logs, cross-reference join/leave timestamps, and build custom spreadsheets.
- **Awkward collection in chat:** Admins frequently have to remind and chase squad members for individual contributions.

### The SquadPay Solution
SquadPay automates this entire pipeline:
1. **Upload Logs:** Ingest raw server console logs (`.log`, `.txt`).
2. **AI Extraction:** Intelligently extract active player playtime using **Google Gemini** or local **Ollama** models.
3. **Proportional Math:** Distribute hosting invoices strictly in proportion to each player's play hours, with strict penny reconciliation.
4. **PayPal Settlement:** Automatically create individual PayPal Sandbox invoices and payment checkout requests for every player with one click.

---

## ⚙️ How SquadPay Works

```
┌─────────────────────────┐
│   Raw Server Logs       │
│ (Minecraft, Rust, etc.) │
└───────────┬─────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────┐
│               AI Parsing Engine                        │
│  - Google Gemini API (gemini-2.5-flash)                │
│  - Local Ollama (qwen2.5-coder:7b)                     │
│  - Deterministic Timestamp Fallback                    │
└───────────┬────────────────────────────────────────────┘
            │  Structured Output: {"PlayerA": 12.5, "PlayerB": 6.2}
            ▼
┌────────────────────────────────────────────────────────┐
│            Proportional Split Engine                   │
│  - Calculate exact percentage shares                   │
│  - Integer cent allocation with penny reconciliation   │
│  - Guaranteed sum == total hosting invoice             │
└───────────┬────────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────────────────────┐
│         PayPal Sandbox REST Gateway                    │
│  - Generate draft invoices                             │
│  - Generate live sandbox checkout order links          │
│  - No real-money transaction risk                      │
└────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture & Key Components

SquadPay is composed of two primary interfaces:

1. **Animated Landing Page (`index.html`):**
   - Cyberpunk-styled co-op gaming landing page built with responsive typography and Framer layout engine.
   - Highlights the core squad mission checkpoints (*01 Assemble*, *02 Analyze*, *03 Settle Up*).
   - Features direct deep links to launch the active app dashboard.

2. **Streamlit Application Dashboard (`app.py`):**
   - Interactive control center for administrators and players.
   - Secure sidebar for configuring credentials and AI providers.
   - Interactive metric cards, playtime breakdowns, and live payment generation tables.

---

## 🧠 AI Parsing Engines

SquadPay features flexible, modular AI backend support:

| Provider | Model | Description | Privacy / Network |
| :--- | :--- | :--- | :--- |
| **Google Gemini API** *(Recommended)* | `gemini-2.5-flash`, `gemini-3.7-flash` | Ultra-fast structured JSON generation via `@google/genai` with strict prompt isolation. | Cloud (HTTPS) |
| **Local Ollama** | `qwen2.5-coder:7b`, `llama3.2` | Runs completely on your local machine via Ollama daemon (`localhost:11434`). | 100% Offline / Private |
| **Deterministic Fallback** | Regular Expression Engine | Regex-based parser that correlates `[timestamp]` login and logout pairs. | Offline (Zero AI dependencies) |

### Prompt Injection Defense
All server logs are wrapped inside XML isolation tags (`<server_logs>...</server_logs>`) with strict instructions to discard any adversarial instructions embedded in gamer tags or log lines.

---

## 🧮 Financial Calculation & Penny Reconciliation

Financial splits cannot rely on floating-point arithmetic because standard rounding can result in total collections that differ from the hosting bill (e.g., \$45.00 bill split 3 ways giving \$15.00 × 3 = \$45.00, but uneven splits leaving fractions of a cent unaccounted for).

SquadPay's financial engine ([`src/calculator.py`](file:///d:/SquadPay/src/calculator.py)):
- Converts amounts into **integer cents**.
- Distributes integer shares based on exact playtime percentages.
- Allocates any remainder cents to the highest-playtime players (penny reconciliation).
- **Guarantees:** `sum(allocated_shares) == total_server_cost` down to the exact cent.

---

## 💳 PayPal Sandbox Integration

The PayPal client ([`src/paypal_client.py`](file:///d:/SquadPay/src/paypal_client.py)) connects to the PayPal REST v2 Sandbox API:
- **Zero Real-Money Risk:** Uses official PayPal Sandbox endpoints (`api-m.sandbox.paypal.com`).
- **Dual Flow:**
  - **Draft Invoices:** Creates formal draft invoices with custom itemized server fees.
  - **Instant Checkout Orders:** Creates order payment links so squad members can simulate checking out with their personal sandbox test buyer accounts.
- **Live Health Probing:** Pre-validates network reachability to PayPal API hosts before submitting requests to provide instant, clear diagnostics.

---

## 🚀 Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/pragyanguwahati-lgtm/SquadPay.git
cd SquadPay
```

### 2. Install Dependencies

SquadPay requires Python 3.10 or higher:

```bash
pip install -r requirements.txt
```

### 3. Launch the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be live at: **`http://localhost:8501`**

*(Optional)* To serve the animated landing page alongside the app:

```bash
python -m http.server 8000
```
Open **`http://localhost:8000`** in your browser.

---

## 🔐 Configuration & Secrets

You can supply your credentials either directly through the **Streamlit Sidebar UI** or via `.streamlit/secrets.toml`.

### Option A: Via the Web UI Sidebar
- Enter your **Google Gemini API Key** (optional, if using Gemini).
- Enter your **PayPal Sandbox Client ID** and **Client Secret**.
- Enter your **PayPal Sandbox Merchant Email**.
- Alternatively, click **"⚡ Fill Demo Sandbox Keys"** for rapid testing.

### Option B: Via `.streamlit/secrets.toml`
Create a `.streamlit/secrets.toml` file in the root directory (this file is excluded from Git via `.gitignore`):

```toml
GEMINI_API_KEY = "AIzaSy..."
PAYPAL_CLIENT_ID = "your_sandbox_client_id"
PAYPAL_CLIENT_SECRET = "your_sandbox_client_secret"
PAYPAL_MERCHANT_EMAIL = "your_sandbox_merchant@business.example.com"
```

---

## 🧪 Running Automated Tests

SquadPay includes an automated unit test suite covering log parsing, mathematical reconciliation, and PayPal client interactions:

```bash
pytest
```

Run with coverage and verbose test names:

```bash
pytest -v
```

All 18 unit tests validate:
- Zero-cost and zero-playtime edge cases.
- Penny reconciliation across prime numbers and uneven splits.
- Prompt injection isolation and malformed log error recovery.
- PayPal OAuth token caching and sandbox draft creation.

---

## 🛡️ Security & Privacy Architecture

- **Ephemeral Storage:** All uploaded log files are processed in-memory via `io.BytesIO`. No log files or player data are ever written to disk.
- **Zero Database Attack Surface:** SquadPay does not require an external database. State resides entirely within the active browser session.
- **Credential Scrubbing:** API secrets and authorization bearer tokens are masked in the UI and automatically scrubbed from error logs.
- **Local AI Privacy Mode:** When using local Ollama (`qwen2.5-coder:7b`), server logs and gamer tags never leave your physical machine.

---

## 📁 Project Directory Layout

```text
SquadPay/
├── index.html                     # Animated cyberpunk landing page
├── app.py                         # Main Streamlit web application & UI
├── requirements.txt               # Production Python dependencies
├── sample_log.txt                 # Realistic sample Minecraft/Palworld server log
├── pytest.ini                     # Pytest testing configuration
├── LICENSE                        # MIT Open-Source License
├── README.md                      # Project documentation and architecture guide
├── .gitignore                     # Git ignore rules for caches & secrets
├── src/
│   ├── __init__.py                # Package initialization
│   ├── parser.py                  # AI & deterministic server log parsing engine
│   ├── calculator.py              # Proportional billing & penny reconciliation
│   └── paypal_client.py           # PayPal Sandbox REST API client
└── tests/
    ├── test_calculator.py         # Unit tests for financial splitting & math
    ├── test_parser.py             # Unit tests for AI and fallback log parsing
    └── test_paypal_client.py      # Unit tests for PayPal sandbox connectivity
```

---

## ⚖️ License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.
