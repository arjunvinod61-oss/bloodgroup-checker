import streamlit as st
import pandas as pd
from bloodgroup_checker import check_compatibility, get_universal_status, BloodGroupAnalyzer, BloodGroupProfile, BloodType, RhType

st.set_page_config(page_title="HemaCheck | Blood Group Explorer", page_icon="🩸", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(145deg,#fffaf8 0%,#f8f2ee 55%,#f4e9e5 100%);}
.block-container {padding-top:2rem;max-width:1250px;}
.hero {background:#421f2b;color:#fff7f3;padding:30px 34px;border-radius:22px;margin-bottom:24px;box-shadow:0 12px 32px #421f2b20;}
.hero h1 {font-family:'Playfair Display',serif;font-size:2.5rem;margin:0;}
.hero p {color:#f1d9d5;margin:8px 0 0;font-size:1rem;}
.metric {background:#fff;border:1px solid #eadbd5;border-radius:16px;padding:18px 20px;}
.metric small {color:#8b6b68;text-transform:uppercase;letter-spacing:.08em;font-weight:700;}
.metric strong {display:block;color:#421f2b;font-size:1.8rem;margin-top:5px;}
.result-good {background:#e6f3ec;border-left:5px solid #347a58;padding:18px;border-radius:12px;color:#174b34;}
.result-bad {background:#fbe9e6;border-left:5px solid #b84e43;padding:18px;border-radius:12px;color:#762c27;}
.note {background:#fff4df;border:1px solid #eed6a6;padding:15px 18px;border-radius:12px;color:#654b20;}
div[data-testid="stTabs"] button {font-weight:700;}

/* HemaCheck: enforce readable light-theme text */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    color-scheme: light !important;
    color: #421f2b !important;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stWidgetLabel"] {
    color: #421f2b !important;
}

.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p {
    color: #795c5c !important;
}

div[data-testid="stTabs"] button {
    color: #65434b !important;
    opacity: 1 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #c52f50 !important;
}

.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] * {
    color: #421f2b !important;
}

/* ===== HemaCheck final visual corrections ===== */

/* Restore the white HemaCheck title */
.hero h1 {
    color: #fff8f3 !important;
}

.hero p {
    color: #f1d9d5 !important;
}

/* Fix dark warning and information boxes */
div[data-testid="stAlert"] {
    background: #fff1df !important;
    border: 1px solid #ead6b8 !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"],
div[data-testid="stAlert"] * {
    color: #5b382e !important;
}

/* Make donor and recipient dropdowns light */
.stApp [data-baseweb="select"] > div {
    background-color: #fffaf7 !important;
    border: 1px solid #d9c4bd !important;
}

.stApp [data-baseweb="select"] * {
    color: #421f2b !important;
}

/* Dropdown options */
div[role="listbox"] {
    background-color: #fffaf7 !important;
}

div[role="option"] {
    color: #421f2b !important;
}

/* Keep the page background light */
.stApp {
    background: linear-gradient(
        145deg,
        #fffaf8 0%,
        #f8f2ee 55%,
        #f4e9e5 100%
    ) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero">
<h1>🩸 HemaCheck</h1>
<p>Blood group compatibility explorer · ABO & RhD educational reference</p>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="note"><b>Educational use only.</b> This tool applies simplified ABO/RhD red-cell rules. It does not perform blood typing, antibody screening, extended-antigen matching or serologic crossmatching. Never use it to decide or authorize a transfusion.</div>', unsafe_allow_html=True)
st.write("")

groups = ["O", "A", "B", "AB"]
rh_values = ["+", "-"]
tab1, tab2, tab3, tab4 = st.tabs(["Compatibility checker", "Compatibility matrix", "Blood type reference", "About & limitations"])

with tab1:
    st.subheader("Check a donor → recipient pairing")
    st.caption("Select the donor and recipient blood groups to see the simplified red-cell compatibility rule.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Donor")
        d_abo = st.selectbox("Donor ABO group", groups, index=0, key="dabo")
        d_rh = st.radio("Donor RhD", rh_values, horizontal=True, key="drh")
        st.markdown(f'<div class="metric"><small>Donor blood type</small><strong>{d_abo}{d_rh}</strong></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("#### Recipient")
        r_abo = st.selectbox("Recipient ABO group", groups, index=1, key="rabo")
        r_rh = st.radio("Recipient RhD", rh_values, horizontal=True, key="rrh")
        st.markdown(f'<div class="metric"><small>Recipient blood type</small><strong>{r_abo}{r_rh}</strong></div>', unsafe_allow_html=True)
    result = check_compatibility(d_abo, d_rh, r_abo, r_rh)
    st.divider()
    if result["compatible"]:
        st.markdown(f'<div class="result-good"><h3>✓ ABO/RhD rule-compatible</h3><b>{result["donor"]} → {result["recipient"]}</b><br>{result["reason"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-bad"><h3>✕ ABO/RhD rule-incompatible</h3><b>{result["donor"]} → {result["recipient"]}</b><br>{result["reason"]}</div>', unsafe_allow_html=True)
    if result["additional_notes"]:
        for note in result["additional_notes"]:
            st.caption("• " + note)
    st.info("A rule-compatible result is not proof that two blood samples are clinically compatible. Actual transfusion requires laboratory testing and clinical oversight.")

with tab2:
    st.subheader("Red-cell compatibility matrix")
    st.caption("Rows are donor types; columns are recipient types. Green indicates compatibility under simplified ABO/RhD rules.")
    all_types = [a+r for a in groups for r in rh_values]
    matrix = []
    for donor in all_types:
        row = {"Donor ↓ / Recipient →": donor}
        for recipient in all_types:
            row[recipient] = "✓" if check_compatibility(donor[:-1],donor[-1],recipient[:-1],recipient[-1])["compatible"] else "—"
        matrix.append(row)
    st.dataframe(pd.DataFrame(matrix).set_index("Donor ↓ / Recipient →"), use_container_width=True)
    st.caption("✓ = rule-compatible · — = rule-incompatible. This is an educational reference, not a crossmatch result.")

with tab3:
    st.subheader("ABO and RhD overview")
    info = {
        "O−": ("No A, B or D antigens on red cells", "Usual universal red-cell donor type"),
        "O+": ("No A or B antigens; D antigen present", "Can donate red cells to Rh-positive recipients of any ABO group"),
        "A−": ("A antigen; D antigen absent", "Can donate red cells to A and AB recipients, subject to RhD rules"),
        "A+": ("A and D antigens", "Can donate red cells to A+ and AB+ recipients"),
        "B−": ("B antigen; D antigen absent", "Can donate red cells to B and AB recipients, subject to RhD rules"),
        "B+": ("B and D antigens", "Can donate red cells to B+ and AB+ recipients"),
        "AB−": ("A and B antigens; D antigen absent", "Can donate red cells to AB− and AB+ recipients"),
        "AB+": ("A, B and D antigens", "Usual universal red-cell recipient type"),
    }
    cols = st.columns(4)
    for i, (blood, (antigens, note)) in enumerate(info.items()):
        with cols[i%4]:
            st.markdown(f'<div class="metric"><small>Blood type</small><strong>{blood}</strong><p>{antigens}</p><small>{note}</small></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("**Important distinction:** O− is commonly called the universal red-cell donor, while AB+ is the universal red-cell recipient. For plasma, the ABO relationship is different: AB plasma is the usual universal plasma donor.")

with tab4:
    st.subheader("Project scope")
    st.markdown("""
**Included**
- ABO red-cell compatibility rules.
- RhD-positive / RhD-negative red-cell compatibility rules.
- Eight-type donor-to-recipient compatibility matrix.
- Educational blood-type reference.

**Not included**
- Actual laboratory blood typing or phenotype/genotype prediction.
- Antibody screening, antibody history or serologic crossmatching.
- Reliable extended-antigen compatibility decisions (Kell, Duffy, Kidd, MNS, etc.).
- Emergency-release decisions or patient-specific clinical recommendations.
- Validated epidemiological prevalence estimates.

**Why this matters:** A person's RhD-negative status does not mean they automatically have anti-D antibodies. Anti-D can develop after exposure. Other clinically significant antibodies and many non-ABO antigens also affect transfusion decisions.
""")
    st.caption("The source project contains extended antigen and population data that are illustrative and not validated here as a clinical reference dataset.")

st.markdown("---")
st.caption("HemaCheck · Educational software demonstration · Not for diagnosis, treatment or transfusion decisions")
