# HemaCheck — Blood Group Compatibility Explorer

A Streamlit educational dashboard and Python package demonstrating simplified ABO/RhD red-cell compatibility.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests
```bash
pytest -q
```

## Google Colab
Upload this ZIP to Colab, unzip it, install requirements, then launch Streamlit using a tunnel. See `COLAB_GUIDE.md`.

## Public deployment
Push this project to a GitHub repository and deploy `app.py` using Streamlit Community Cloud. See `DEPLOY_GUIDE.md`.

## Safety and scope
Educational demonstration only. A rule-compatible result is not transfusion clearance. Real transfusions require validated laboratory blood grouping, antibody screening and serologic crossmatching, interpreted by qualified professionals. No clinical decisions should be based on this app.

## Project structure
- `app.py` — Streamlit dashboard
- `bloodgroup_checker/` — Python library
- `tests/` — automated tests
- `requirements.txt` — runtime dependencies
