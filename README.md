# 🎮 Proportional Squad-Pay

> **Fair server bill splitting for multiplayer gaming squads powered by local AI and PayPal.**  
> *Submitted to the PayPal AI Hackathon 2026.*

---

## 🌟 Overview & Inspiration

Multiplayer squads (Minecraft, Palworld, Rust, ARK) love running dedicated servers, but monthly hosting invoices always create friction:
- *Why should someone who played 2 hours pay the same as someone who played 40 hours?*
- *Why should server admins spend hours manually inspecting console logs and reconciling spreadsheets?*

**Proportional Squad-Pay** solves this end-to-end:
1. It ingests raw game server logs.
2. It uses **local AI (Ollama with `qwen2.5-coder:7b`)** to calculate exact player playtime without transmitting gaming data to third-party cloud APIs.
3. It uses the **PayPal Sandbox REST API** to automatically generate proportional draft payment requests for each squad member.

---

## 🔒 Privacy & Financial Architecture

- **Local AI for Privacy:** Raw game logs, player gamer tags, and server IP addresses remain strictly on the user's local machine. The local `qwen2.5-coder:7b` LLM parses timestamps without sending private data to cloud providers.
- **PayPal Sandbox for Financial Routing:** Automatically generates draft invoices via `paypalrestsdk` in Sandbox mode. Each player receives a fair invoice directly proportional to their playtime.
- **Local-First, Ephemeral Security:** No database, no user tracking, no hardcoded API keys. All credentials reside only in RAM during the active session.

---

## 🚀 Quickstart for Hackathon Judges (Exactly 3 Commands)

To run the application locally, execute the following 3 terminal commands:

```bash
pip install -r requirements.txt
```

```bash
ollama run qwen2.5-coder:7b
```

```bash
streamlit run app.py
```

*(Note: The landing page can be viewed directly by opening `index.html` in any browser, or click "START THE QUEST" to enter the Streamlit app at `http://localhost:8501`)*

---

## 🛠️ How It Works (Step-by-Step)

1. **Enter Sandbox Credentials:** Input your PayPal Sandbox Client ID and Secret in the secure sidebar (or click **"Fill Demo Sandbox Keys"** for rapid evaluation).
2. **Set Hosting Cost:** Enter the monthly server hosting bill (e.g., `$45.00`).
3. **Upload Log:** Upload a server log (`.txt` or `.log`), or check **"use bundled sample"** to test with the provided 15-line `sample_log.txt`.
4. **Execute Quest:**
   - **Parser (`src/parser.py`):** Local Qwen 2.5 Coder analyzes join/leave events and outputs strict JSON `{"player_name": hours}`.
   - **Calculator (`src/calculator.py`):** Computes exact percentages `(player_hours / total_hours) * total_cost` with penny reconciliation.
   - **PayPal Client (`src/paypal_client.py`):** Triggers `paypalrestsdk.Invoice` in Sandbox mode and generates draft invoice IDs.
5. **Success Banner:** View the generated Sandbox Invoice IDs and copy them directly.

---

## 🛡️ 36-Point Security Compliance

This project implements a rigorous 36-point security model:
- **No Hardcoded Secrets (Vector 3):** Credentials injected via session state password inputs.
- **Zero DB Attack Surface (Vectors 1, 7, 17, 18):** Ephemeral architecture eliminates SQL/NoSQL injection and RLS vulnerabilities.
- **Prompt Injection Isolation (Vector 34):** Untrusted log files are isolated within strict XML boundary tags and instructed to produce JSON only.
- **RAM-Only File Handling (Vectors 21, 22):** Files are parsed from memory `BytesIO` streams; no user files are saved to disk.
- **Rate-Limiting & Secret Scrubbing (Vectors 11, 28):** Error logs scrub API secrets, and calls are throttled with a `0.5s` delay buffer.

---

## 📦 Project Structure

```text
SquadPay/
├── index.html                 # Cyberpunk landing page ("START THE QUEST")
├── app.py                     # Streamlit application dashboard
├── requirements.txt           # Dependencies (streamlit, paypalrestsdk, ollama)
├── sample_log.txt             # Realistic 15-line test server log
├── LICENSE                    # MIT License
├── README.md                  # Devpost documentation & judge quickstart
├── .gitignore                 # Excludes cache and secrets
├── src/
│   ├── parser.py              # Ollama qwen2.5-coder:7b log parsing engine
│   ├── calculator.py          # Proportional math & penny reconciliation
│   └── paypal_client.py       # PayPal REST SDK Sandbox integration
└── docs/                      # Architectural specifications & security policies
    ├── PRD.md
    ├── architecture.md
    ├── design.md
    ├── memory.md
    ├── security.md
    ├── Auth.md
    ├── Data Security.md
    ├── Threat model.md
    └── Security checklist.md
```

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for details.
