# Data Security & Integrity (`Data Security.md`)

## 1. Overview
Financial data (PayPal invoices) and gaming data (server logs) must be protected. This app processes all data locally and only communicates with the official PayPal Sandbox API.

## 2. Addressed Threat Vectors
- **Exposed DB Credentials, Open DB Permissions, Row Level Security:** Mitigated by design. There is no database.
- **Hardcoded Secrets & Public `.env` files:** No secrets exist in the codebase. `.gitignore` prevents `.env` accidental commits.
- **Secrets in Git & Secrets in JS:** Handled exclusively in Python memory; frontend JavaScript/HTML is fully static.
- **Input Validation:** All uploaded game logs (`.txt`, `.log`) are strictly parsed as strings.
- **SQL / NoSQL Injection:** Impossible by design (no database queries).
- **Insecure File Uploads & Path Traversal:** Streamlit's `st.file_uploader` securely reads files directly into RAM as `BytesIO` objects. No files are saved to the local file system.

## 3. Data Processing Flow (Ollama)
1. The user uploads `server.log`.
2. The file is held in RAM.
3. The Python backend sends the text to the local `qwen2.5-coder:7b` model via `localhost:11434`.
4. The model returns a JSON payload. 
5. The raw log data **never leaves the user's machine**, ensuring zero privacy leakage to cloud AI providers.