# Project Memory & State (`memory.md`)

## 1. Project Context
**Project:** Proportional Squad-Pay
**Objective:** Build a local web application that calculates proportional multiplayer server costs based on parsed game logs and generates individual PayPal payment requests.
**Event:** PayPal AI Hackathon (Deadline: November 12, 2026).
**Core Directive:** The application must prove the seamless integration of AI (log parsing) and PayPal (invoicing/orders) while remaining highly testable for judges (local execution, open-source MIT license).

## 2. Key Architectural Decisions
- **Privacy-First AI:** Chosen `ollama` with `qwen2.5-coder:7b` to ensure raw gaming logs are processed entirely on the user's local machine. No data is sent to cloud LLM providers.
- **Financial Engine:** Chosen `paypalrestsdk` operating strictly in `sandbox` mode. App will dynamically generate Sandbox Invoice IDs to prove API execution without using real money.
- **Dual-Interface Structure:** 
  - **Landing Page:** A high-performance HTML/CSS entry point utilizing `liquidGL`, `unlumen ui`, and `animaster lib` for a slick, cyberpunk/gamer aesthetic.
  - **Application Dashboard:** A Streamlit Python backend for handling the actual file uploads, AI processing, and PayPal API execution.
- **Ephemeral State:** Streamlit session state is used in place of a database to keep the local deployment lightweight and judge-friendly.

## 3. Current Progress (as of Oct 2026)
- [x] Hackathon pivot and project selection complete.
- [x] `PRD.md` drafted.
- [x] `architecture.md` drafted.
- [x] `design.md` drafted (HTML baseline established with Squadpay branding).
- [x] `security.md` drafted and mitigated 36 threat vectors.
- [x] `memory.md` (This file) established for agent tracking.
- [x] Security documentation completed (`Auth.md`, `Data Security.md`, etc.).
- [ ] Code scaffolding (Streamlit + UI integration).
- [ ] PayPal Sandbox account creation & testing.
- [ ] Video demo recording.

## 4. Known Constraints & Workarounds
- **Hackathon Rule - Open Source:** Must include an `MIT` or `Apache 2.0` license in the root directory.
- **Hackathon Rule - Testing:** Judges must be able to run it. We will provide a `sample_log.txt` in the repository so they do not need to generate their own game server logs to test the AI.
- **UI Translation:** The slick HTML/WebGL landing page needs to seamlessly route the user into the Streamlit functional dashboard once they click "START THE QUEST".

## 5. Next Immediate Steps for Agent
1. Initialize the Git repository with the correct `.gitignore` and `LICENSE`.
2. Scaffold the base Streamlit application (`app.py`) and integrate the provided HTML design files.