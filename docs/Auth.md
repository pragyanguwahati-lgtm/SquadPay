# Authentication & Authorization (`Auth.md`)

## 1. Overview
The Proportional Squad-Pay app uses a **single-tenant, ephemeral authentication** model. Because this is a local application designed for a hackathon, there is no central user database. The "user" is the person running the Python environment locally.

## 2. Addressed Threat Vectors
- **API Key Authentication:** Handled via Streamlit's `st.text_input(type="password")`. Keys are never saved to disk.
- **Weak Auth & Broken Password Reset:** Mitigated by design (no user accounts).
- **Missing Authz Check & Unprotected Admin Route:** The local runner is the sole admin. No remote admin routes exist.
- **Cross User Access & IDOR / BOLA:** Impossible by design; the app only serves one local user per runtime session.
- **Weak Session Mgmt & JWT Secrets:** The app relies on Streamlit's internal memory (`st.session_state`). No JWTs or persistent session cookies are issued to a browser.
- **Default Credentials:** None used. The app requires the user to input their own valid PayPal Sandbox API keys to function.

## 3. PayPal Sandbox Authentication
1. User inputs `PAYPAL_CLIENT_ID` and `PAYPAL_CLIENT_SECRET` into the UI sidebar.
2. The app stores these in `st.session_state` for the duration of the browser tab's life.
3. The app authenticates with the `paypalrestsdk` module using `mode="sandbox"`.
4. Upon browser refresh or app termination, the keys are completely wiped from memory.