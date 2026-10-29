# System Architecture

## 1. Technology Stack
- **Frontend & Routing:** Streamlit (Python)
- **Backend Language:** Python 3.10+
- **AI Engine:** Ollama (Local runtime) via the `ollama` Python client
- **AI Model:** `qwen2.5-coder:7b` (Provides 32k context window and high JSON compliance)
- **External API:** PayPal REST SDK (`paypalrestsdk`) operating strictly in `sandbox` mode

## 2. Component Architecture
The application follows a modular, serverless-style architecture optimized for local execution.

### A. User Interface Layer (`app.py`)
- Manages Streamlit session state.
- Handles file uploads (`.txt`/`.log`).
- Captures secure user inputs (PayPal Client ID/Secret) via Streamlit sidebar.
- Renders data tables and action buttons.

### B. AI Parsing Engine (`parser.py`)
- Constructs the prompt dynamically by wrapping the uploaded server log.
- Forces the LLM to output a strict JSON schema: `{"players": [{"name": "string", "hours": float}]}`.
- Handles Ollama API timeouts or malformed JSON retries.

### C. Financial Calculator (`calculator.py`)
- Receives the total server cost and the JSON playtime payload.
- Calculates percentages: `(Player Hours / Total Hours) * Total Cost`.
- Formats outputs to two decimal places (e.g., `12.50`) to comply with PayPal API currency standards.

### D. Payment Integration (`paypal_client.py`)
- Authenticates using the injected Client ID and Secret.
- Iterates through the calculated list.
- Constructs the JSON payload required by `paypalrestsdk.Invoice`.
- Executes the API calls and returns the generated `invoice_id` strings to the UI.

## 3. Data Flow
1. **Input:** `server.log` -> Streamlit `st.file_uploader` (InMemoryUploadedFile).
2. **Processing (AI):** Log text -> `ollama.chat()` -> Local Qwen 2.5 Coder -> JSON array.
3. **Processing (Math):** JSON array + Total Cost -> Python Dictionary with calculated `$ amount_owed`.
4. **Output (API):** Dictionary -> `paypalrestsdk.Invoice.create()` -> Sandbox Invoice Drafts.
5. **UI Rendering:** Draft IDs displayed in Streamlit success banners.

## 4. Expected Directory Structure
```text
paypal-squad-pay/
├── app.py                 # Main Streamlit UI
├── src/
│   ├── parser.py          # Ollama integration logic
│   ├── calculator.py      # Math and cost splitting logic
│   └── paypal_client.py   # PayPal REST SDK integration
├── requirements.txt       # Dependencies
├── LICENSE                # MIT License
├── sample_log.txt         # Mock data for testing
└── docs/
    ├── PRD.md
    └── architecture.md
```