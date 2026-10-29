# Security & Threat Mitigation Policies

This document outlines the security posture for the **Proportional Squad-Pay** application. Because this app handles financial integrations (PayPal) and user activity logs, security is prioritized through a **Local-First, Ephemeral Architecture**.

Below is the mitigation strategy for the 36 critical security vectors identified for this project.

## 1. Secrets Management & Authentication

* **API Key Authentication:** PayPal Client ID and Secret are strictly required for invoicing. They are authenticated dynamically per session.
* **Hardcoded Secrets & Exposed DB Credentials:** No API keys, database URIs, or tokens will ever be hardcoded in the source code.
* **Public `.env` Files & Secrets in Git:** The `.gitignore` file explicitly blocks `.env` files and `__pycache__` from being committed to the repository.
* **Secrets in JS & Exposed Source Maps:** No secrets are handled on the frontend. The HTML landing page contains only static assets. All PayPal authentication happens server-side in Python.
* **JWT Secrets & Weak Session Mgmt:** The app relies on Streamlit's ephemeral session state rather than persistent JWTs, mitigating token theft across sessions.
* **Default Credentials:** Not applicable; the system requires the user to input their own PayPal Sandbox keys.

## 2. Database & Access Control

*Because this application uses an ephemeral architecture without a persistent database, several traditional attack vectors are inherently neutralized.*

* **Row Level Security (RLS) & Open DB Permissions:** Mitigated by design (No persistent database).
* **SQL Injection & NoSQL Injection:** Mitigated by design (No database queries executed).
* **Cross User Access & IDOR / BOLA:** Mitigated by design. This is a single-tenant, locally run application. One user per localhost session means cross-tenant data leakage is impossible.
* **Missing Authz Check & Unprotected Admin Route:** The user running the local Python environment acts as the sole administrator of their session.
* **Weak Auth & Broken Password Reset:** No user accounts are stored or managed by the app.

## 3. Data Input & Execution Vectors

* **Input Validation & APIs + User Input:** All uploaded log files are strictly validated. The prompt sent to the Ollama model is hard-templated to prevent the user's log file from hijacking the core prompt instructions (Prompt Injection mitigation).
* **Insecure File Uploads & Path Traversal:** The Streamlit `st.file_uploader` is restricted explicitly to `.txt` and `.log` MIME types. Uploaded files are kept in memory and are not saved to the local file system, preventing malicious executable execution or directory traversal.
* **XSS (Cross-Site Scripting) & CSRF:** Handled natively by Streamlit's frontend sanitization.
* **SSRF (Server-Side Request Forgery):** The application only makes outbound HTTP requests to two explicit endpoints: local Ollama (`localhost:11434`) and the official PayPal Sandbox API. Dynamic URL routing is prohibited.

## 4. Financial & Payment Integrity

* **FE (Front-End) Payment Checks:** Financial math (total cost / total hours) is executed strictly on the Python backend. Users cannot manipulate network requests to alter the PayPal invoice amounts via browser dev tools.
* **Unsigned Webhooks:** Invoices are generated via outbound REST API calls. No inbound webhooks are exposed, removing the risk of forged payment confirmations.

## 5. Infrastructure, Logs & Environment

* **Exposed Environments & Cloud Service Misconfig:** The app is designed to run locally, eliminating cloud misconfigurations.
* **Logs Leak Secrets & Exposed Logs:** The `paypalrestsdk` execution will be wrapped in try/except blocks that explicitly scrub or omit the Client ID/Secret if an error is printed to the terminal.
* **Verbose Prod Errors & Exposed Prod Debug Tools:** Streamlit will be configured to hide traceback details in the UI (preventing internal path leaks).
* **Rate Limits:** Outbound calls to PayPal are batched and processed sequentially to avoid hitting Sandbox API rate limits.
* **Permissive CORS:** Streamlit's default CORS policies apply, preventing unauthorized cross-origin requests to the local server port.
* **Client-Only Security:** Security validation occurs strictly in the Python backend, never relying on HTML/JS-only checks.