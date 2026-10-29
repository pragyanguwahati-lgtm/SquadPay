# Product Requirements Document (PRD)

## 1. Project Overview
**Project Name:** Proportional Squad-Pay
**Target Hackathon:** PayPal AI Hackathon (Deadline: Nov 12, 2026)
**Core Concept:** A web application that ingests raw multiplayer game server logs, uses local AI to calculate precise player activity times, and leverages the PayPal REST SDK to generate proportional payment requests for shared server costs.

## 2. Target Audience
- Multiplayer gaming squads (Minecraft, Rust, Palworld, etc.).
- Clan leaders and server administrators who manage monthly hosting invoices.

## 3. Core Features & Requirements
- **Secure Credential Management:** Local session UI for entering PayPal Sandbox API keys (no hardcoding).
- **Log Ingestion:** Streamlit file uploader accepting `.txt` and `.log` server files.
- **Privacy-First AI Parsing:** Integration with Ollama (`qwen2.5-coder:7b`) to securely extract player join/leave timestamps locally without transmitting gaming data to third-party cloud APIs.
- **Dynamic Cost Calculation:** Algorithmic conversion of total server cost into proportional player shares based on exact hours played.
- **Automated Invoicing:** One-click execution of the PayPal Invoicing API to generate sandbox drafts for each player.

## 4. User Flow
1. User enters PayPal Sandbox Client ID and Secret in the sidebar.
2. User inputs the total monthly server bill (e.g., $45.00).
3. User uploads the server log file.
4. UI displays a loading spinner while the local Ollama agent parses the log.
5. UI displays a data table showing: `Player Name | Hours Played | % of Total | Amount Owed`.
6. User clicks "Generate PayPal Requests".
7. UI iterates through the table, hits the PayPal API, and displays the generated Invoice IDs.

## 5. Out of Scope (Hackathon Constraints)
- Production PayPal deployment (Restricted to Sandbox mode).
- Persistent database storage (App will use Streamlit's ephemeral session state).
- Live server RCON integration (Data ingestion via manual file upload only).