# Horizon v24 — Railway deployment

The included `Procfile` starts Streamlit on Railway's assigned port. Connect the repository to Railway and use the `web` process defined in the Procfile.

If a manual start command is required:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

The application reads `majors.json` and `academic_sources.json` from `data/` first, then falls back to the project root. Both copies are kept synchronized in this release.

**Privacy:** a private GitHub repository does not make the deployed URL private. Configure an access-control layer and test it before inviting students. Do not store personal student data in this prototype.
