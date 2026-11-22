# Horizon v24 — Private Testing Deployment Guide

## Before deployment
1. Keep the GitHub repository private.
2. Do not upload student names, email addresses, survey answers, assessment records or other personal data to the repository.
3. The Reflection journal is session-based in this prototype and is not a secure permanent student-record system. Do not use it for sensitive notes.
4. Do not commit passwords, API keys, `.env` files or hosting secrets.
5. A private GitHub repository does not make the deployed website private. Configure app-level or hosting-level access restrictions and test them from a separate browser session before inviting anyone.

## Deploy with Railway
1. Create a private GitHub repository and upload the contents of this project folder to its root.
2. Confirm `app.py`, `requirements.txt`, `Procfile`, `data/` and `horizon_logo.svg` are at repository root.
3. Connect the private repository to Railway.
4. Railway should use the included `Procfile`. If a start command is required, use:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

5. Add an access-control layer before sharing the site. A generated URL may otherwise be publicly reachable.
6. Test language switching, subject selection, network generation, major details, comparison, reflection and mobile layout.
7. Invite only a small group of trusted testers after confirming access restrictions.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Important limitations
- This prototype does not provide student accounts or a secure database.
- Reflection entries are not guaranteed to persist between sessions.
- Do not collect sensitive personal data through this prototype.
- Review hosting costs and access settings before enabling public traffic.
