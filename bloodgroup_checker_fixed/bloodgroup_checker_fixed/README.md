# HemaCheck — Blood Group Compatibility Explorer

A Streamlit educational dashboard and Python package for ABO/RhD red-cell compatibility, inheritance exploration, antigen-system learning, rare phenotype education and knowledge assessment.

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

## Dashboard modules
- Compatibility checker and 8 × 8 red-cell matrix.
- ABO/RhD reference cards.
- Inheritance Lab: enumerates possible child phenotypes from parent phenotypes. It avoids assigning one probability when parental genotypes are unknown.
- Antigen Explorer: educational summaries of ABO, Rh, Kell, Duffy, Kidd and MNS systems.
- Rare Phenotypes: educational summaries of Bombay, Rh-null, Duffy-null and para-Bombay phenotypes.
- Knowledge Quiz with explanations.

## Safety and scope
Educational demonstration only. A rule-compatible result is not transfusion clearance. Real transfusions require validated laboratory blood grouping, antibody screening and serologic crossmatching, interpreted by qualified professionals. No clinical decisions should be based on this app.

- `bloodgroup_checker/education.py` — phenotype-based Mendelian possibility helpers
- `tests/test_education.py` — inheritance tests

## Project structure
- `app.py` — Streamlit dashboard
- `bloodgroup_checker/` — Python library
- `tests/` — automated tests
- `requirements.txt` — runtime dependencies
