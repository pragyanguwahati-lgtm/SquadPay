# Hackathon Security Checklist

Before recording the demo video and submitting the GitHub repository, ensure all 36 threat vectors are mitigated.

## Authentication & Authorization
- [x] 2. Public `.env` files (Added to `.gitignore`)
- [x] 3. Hardcoded secrets (API keys passed via UI only)
- [x] 4. Weak auth (N/A - Ephemeral session)
- [x] 5. Missing Authz check (N/A - Local runner is admin)
- [x] 6. Cross user access (N/A - Single-tenant)
- [x] 24. Broken password reset (N/A)
- [x] 25. Weak session mgmt (Streamlit in-memory sessions)
- [x] 26. JWT secrets (N/A)
- [x] 30. Default credentials (Requires manual input)
- [x] 33. IDOR / BOLA (N/A)

## Data & Database Integrity
- [x] 1. Row level security (N/A - No DB)
- [x] 7. Open DB permissions (N/A - No DB)
- [x] 17. SQL injection (N/A)
- [x] 18. NoSQL injection (N/A)
- [x] Exposed DB credentials (N/A)

## Infrastructure & Code
- [x] 8. Cloud service misconfig (N/A - Local application)
- [x] 9. Unprotected admin route (N/A)
- [x] 10. Exposed prod debug tools (Streamlit configured securely)
- [x] 11. Logs leak secrets (Try/except blocks scrub PayPal secrets)
- [x] 12. Verbose prod errors (UI tracebacks disabled)
- [x] 13. Secrets in git (Clean repository)
- [x] 14. Secrets in JS (Static frontend)
- [x] 29. Exposed environments (Local execution)
- [x] 35. Exposed logs (Console only, no file logging)
- [x] 36. Exposed source maps (Static HTML)

## Input, Output & Network
- [x] 15. Client-only security (Math verified on Python backend)
- [x] 16. Input validation (Only `.txt`/`.log` files allowed)
- [x] 19. XSS (Streamlit sanitization)
- [x] 20. CSRF (Streamlit websocket security)
- [x] 21. Insecure file uploads (File parsed in RAM via `BytesIO`)
- [x] 22. Path traversal (No files saved to disk)
- [x] 23. SSRF (Hardcoded PayPal / Ollama endpoints)
- [x] 27. Permissive CORS (Streamlit default restrictions)
- [x] 28. Rate limits (Added `time.sleep` between PayPal calls)
- [x] 31. Unsigned webhooks (N/A - Outbound API calls only)
- [x] 32. FE Payment checks (Amounts calculated in Python)
- [x] 34. APIs + user input (Strict Prompt templates to prevent LLM injection)