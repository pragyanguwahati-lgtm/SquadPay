# Threat Model (`Threat model.md`)

## 1. Threat Landscape
As a local application, the primary threat actors are local malware, compromised dependencies, and malicious log files. The application's attack surface includes the UI, the file uploader, and the outbound API requests.

## 2. Addressed Threat Vectors
- **Cloud Service Misconfig & Exposed Environments:** Mitigated by design (local execution only).
- **Logs Leak Secrets & Exposed Logs:** Python `logging` is configured to mask `PAYPAL_CLIENT_SECRET` in any console tracebacks.
- **Verbose Prod Errors & Exposed Prod Debug Tools:** Streamlit's production mode (`--server.headless true`) hides detailed tracebacks from the UI.
- **Client-Only Security:** All cost calculations occur in `calculator.py` on the backend.
- **XSS & CSRF:** Handled by Streamlit's built-in frontend sanitization and websocket security.
- **SSRF (Server-Side Request Forgery):** Outbound requests are hardcoded to PayPal APIs; users cannot manipulate the target URL.
- **Permissive CORS:** Streamlit blocks cross-origin requests by default.
- **Rate Limits:** PayPal API requests are executed iteratively with a `time.sleep(0.5)` buffer to prevent HTTP 429 Too Many Requests errors.
- **Unsigned Webhooks:** We only push data (Invoices) out; we do not accept inbound webhooks.
- **FE Payment Checks:** All financial math is done in Python. A user cannot use Chrome DevTools to change a $24 invoice to $1.
- **APIs + User Input:** LLM Prompts are strictly templated to prevent Prompt Injection from a malicious game log.
- **Exposed Source Maps:** Frontend HTML uses static CSS/JS with no sensitive source maps.