import random
import pandas as pd
import streamlit as st

from bloodgroup_checker import check_compatibility, get_universal_status
from bloodgroup_checker.education import (
    abo_inheritance_scenarios,
    possible_abo_offspring,
    possible_combined_offspring,
)

st.set_page_config(page_title="HemaCheck | Blood Group Explorer", page_icon="🩸", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif; color-scheme:light;}
.stApp {background:linear-gradient(145deg,#fffaf8 0%,#f8f2ee 55%,#f4e9e5 100%); color:#421f2b;}
.block-container {padding-top:2rem;max-width:1250px;}
.hero {background:#421f2b;color:#fff7f3;padding:30px 34px;border-radius:22px;margin-bottom:24px;box-shadow:0 12px 32px #421f2b20;}
.hero h1 {font-family:'Playfair Display',serif;font-size:2.5rem;margin:0;color:#fff8f3 !important;}
.hero p {color:#f1d9d5 !important;margin:8px 0 0;font-size:1rem;}
.metric {background:#fff;border:1px solid #eadbd5;border-radius:16px;padding:18px 20px;}
.metric small {color:#8b6b68;text-transform:uppercase;letter-spacing:.08em;font-weight:700;}
.metric strong {display:block;color:#421f2b;font-size:1.8rem;margin-top:5px;}
.result-good {background:#e6f3ec;border-left:5px solid #347a58;padding:18px;border-radius:12px;color:#174b34;}
.result-bad {background:#fbe9e6;border-left:5px solid #b84e43;padding:18px;border-radius:12px;color:#762c27;}
.note {background:#fff4df;border:1px solid #eed6a6;padding:15px 18px;border-radius:12px;color:#654b20;}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp p,.stApp li,.stApp label,.stApp [data-testid="stWidgetLabel"] {color:#421f2b;}
.stApp [data-testid="stCaptionContainer"],.stApp [data-testid="stCaptionContainer"] p {color:#795c5c;}
div[data-testid="stTabs"] button {font-weight:700;color:#65434b;opacity:1;}
div[data-testid="stTabs"] button[aria-selected="true"] {color:#c52f50;}
.stApp [data-baseweb="select"] > div {background:#fffaf7;border:1px solid #d9c4bd;}
.stApp [data-baseweb="select"] * {color:#421f2b;}
div[role="listbox"] {background:#fffaf7;}
div[role="option"] {color:#421f2b;}
div[data-testid="stAlert"] {background:#fff1df;border:1px solid #ead6b8;border-radius:12px;}
div[data-testid="stAlert"] * {color:#5b382e;}
div[data-testid="stRadio"] label {color:#421f2b;}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><h1>🩸 HemaCheck</h1>
<p>Blood Group Intelligence & Biology Explorer · Educational ABO/RhD reference</p></div>""", unsafe_allow_html=True)
st.markdown('<div class="note"><b>Educational use only.</b> HemaCheck is not a blood-typing, antibody-screening or crossmatching service. Its simplified rules and inheritance models must never be used to make transfusion, pregnancy or other clinical decisions.</div>', unsafe_allow_html=True)
st.write("")

# Compact overview metrics
m1, m2, m3, m4 = st.columns(4)
for col, value, label in [
    (m1, "8", "ABO/RhD phenotypes"),
    (m2, "2", "Core inheritance systems"),
    (m3, "7+", "Extended systems explored"),
    (m4, "4", "Learning modules"),
]:
    with col:
        st.markdown(f'<div class="metric"><small>{label}</small><strong>{value}</strong></div>', unsafe_allow_html=True)
st.write("")

groups = ["O", "A", "B", "AB"]
rh_values = ["+", "-"]
tabs = st.tabs([
    "Compatibility checker", "Compatibility matrix", "Blood type reference",
    "Inheritance lab", "Antigen explorer", "Rare phenotypes", "Knowledge quiz", "About & limitations"
])

with tabs[0]:
    st.subheader("Check a donor → recipient pairing")
    st.caption("Simplified red-cell ABO/RhD rules only. A compatible result is not a clinical crossmatch.")
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
    status = get_universal_status(blood_type=d_abo, rh_str=d_rh)
    st.divider()
    if result["compatible"]:
        st.markdown(f'<div class="result-good"><h3>✓ ABO/RhD rule-compatible</h3><b>{result["donor"]} → {result["recipient"]}</b><br>{result["reason"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-bad"><h3>✕ ABO/RhD rule-incompatible</h3><b>{result["donor"]} → {result["recipient"]}</b><br>{result["reason"]}</div>', unsafe_allow_html=True)
    for note in result.get("additional_notes", []):
        st.caption("• " + note)
    st.info("Actual transfusion compatibility requires validated patient and donor testing, antibody screening and serologic crossmatching.")

with tabs[1]:
    st.subheader("Red-cell compatibility matrix")
    st.caption("Rows are donor types; columns are recipient types. This matrix represents simplified ABO/RhD rules only.")
    all_types = [a + r for a in groups for r in rh_values]
    matrix = []
    for donor in all_types:
        row = {"Donor ↓ / Recipient →": donor}
        for recipient in all_types:
            row[recipient] = "✓" if check_compatibility(donor[:-1], donor[-1], recipient[:-1], recipient[-1])["compatible"] else "—"
        matrix.append(row)
    st.dataframe(pd.DataFrame(matrix).set_index("Donor ↓ / Recipient →"), use_container_width=True)
    st.caption("✓ = rule-compatible · — = rule-incompatible. Not a laboratory crossmatch.")

with tabs[2]:
    st.subheader("ABO and RhD reference")
    info = {
        "O−": ("A, B and D antigens absent", "Usual universal red-cell donor designation"),
        "O+": ("A and B absent; D present", "Can be considered for RhD-positive recipients across ABO groups"),
        "A−": ("A present; D absent", "A antigen; RhD-negative"),
        "A+": ("A and D present", "A antigen; RhD-positive"),
        "B−": ("B present; D absent", "B antigen; RhD-negative"),
        "B+": ("B and D present", "B antigen; RhD-positive"),
        "AB−": ("A and B present; D absent", "AB phenotype; RhD-negative"),
        "AB+": ("A, B and D present", "Usual universal red-cell recipient designation"),
    }
    cols = st.columns(4)
    for i, (blood, (antigens, note)) in enumerate(info.items()):
        with cols[i % 4]:
            st.markdown(f'<div class="metric"><small>Blood type</small><strong>{blood}</strong><p>{antigens}</p><small>{note}</small></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("**Remember:** red-cell and plasma compatibility are different. O− and AB+ labels here refer to red-cell transfusion conventions, not all blood components.")

with tabs[3]:
    st.subheader("Inheritance lab")
    st.write("Explore which ABO/RhD phenotypes could occur in children from two parents. The result lists possibilities; it does not infer a child's actual type.")
    p1, p2 = st.columns(2)
    with p1:
        parent1_abo = st.selectbox("Parent 1 ABO phenotype", groups, key="p1abo")
        parent1_rh = st.selectbox("Parent 1 RhD phenotype", rh_values, key="p1rh")
    with p2:
        parent2_abo = st.selectbox("Parent 2 ABO phenotype", groups, index=1, key="p2abo")
        parent2_rh = st.selectbox("Parent 2 RhD phenotype", rh_values, key="p2rh")
    outcomes = possible_combined_offspring(parent1_abo, parent1_rh, parent2_abo, parent2_rh)
    st.markdown("#### Possible child phenotypes under the simplified model")
    out_cols = st.columns(min(4, max(1, len(outcomes))))
    for i, phenotype in enumerate(outcomes):
        with out_cols[i % len(out_cols)]:
            st.markdown(f'<div class="metric"><small>Possible phenotype</small><strong>{phenotype}</strong></div>', unsafe_allow_html=True)
    st.caption("No single probability is shown because a parent's phenotype may correspond to more than one genotype (for example, A can be AA or AO; RhD-positive can be DD or Dd). The model assumes the usual simplified ABO and D/d inheritance and excludes rare variants, chimerism and other complexities.")
    with st.expander("View ABO genotype scenarios"):
        scenarios = abo_inheritance_scenarios(parent1_abo, parent2_abo)
        rows = []
        for s in scenarios:
            rows.append({
                "Parent 1 genotype scenario": s["parent1_genotype"],
                "Parent 2 genotype scenario": s["parent2_genotype"],
                "Possible offspring ratios in this scenario": ", ".join(f"{k}: {v*100:.0f}%" for k, v in s["offspring_ratios"].items()),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption("Ratios apply only within the displayed genotype scenario, not to phenotype inputs as a whole.")

with tabs[4]:
    st.subheader("Antigen and blood-group systems explorer")
    systems = {
        "ABO": {"antigens": "A and B carbohydrate antigens", "gene": "ABO", "chromosome": "9", "antibodies": "Anti-A and/or anti-B may be present according to ABO type", "importance": "ABO-incompatible red-cell transfusion can cause severe acute hemolytic reactions."},
        "Rh": {"antigens": "D is the most clinically familiar; C, c, E and e are also important", "gene": "RHD and RHCE", "chromosome": "1", "antibodies": "Anti-D and other Rh antibodies can develop after exposure", "importance": "Rh antibodies can be clinically significant in transfusion and pregnancy."},
        "Kell": {"antigens": "K, k and other Kell-system antigens", "gene": "KEL", "chromosome": "7", "antibodies": "Anti-K is clinically significant", "importance": "K antibodies can cause hemolytic transfusion reactions and hemolytic disease of the fetus and newborn."},
        "Duffy": {"antigens": "Fyᵃ and Fyᵇ", "gene": "ACKR1", "chromosome": "1", "antibodies": "Anti-Fyᵃ and anti-Fyᵇ", "importance": "Duffy antigens are relevant to transfusion medicine and have a known relationship with susceptibility to Plasmodium vivax infection."},
        "Kidd": {"antigens": "Jkᵃ and Jkᵇ", "gene": "SLC14A1", "chromosome": "18", "antibodies": "Anti-Jkᵃ and anti-Jkᵇ", "importance": "Kidd antibodies may become difficult to detect over time and are associated with delayed hemolytic transfusion reactions."},
        "MNS": {"antigens": "M, N, S and s among many others", "gene": "GYPA and GYPB", "chromosome": "4", "antibodies": "Examples include anti-M, anti-N, anti-S and anti-s", "importance": "Some MNS antibodies are clinically significant; significance depends on the specific antibody."},
        "Kell/Diego etc.": {"antigens": "Many additional antigens exist across multiple blood-group systems", "gene": "Multiple genes", "chromosome": "Varies", "antibodies": "Antibodies depend on the antigen and exposure history", "importance": "The full ISBT classification contains many systems beyond ABO and Rh."},
    }
    chosen = st.selectbox("Choose a blood-group system", list(systems.keys()))
    data = systems[chosen]
    a, b = st.columns(2)
    with a:
        st.markdown("**Antigens**")
        st.write(data["antigens"])
        st.markdown("**Associated gene(s)**")
        st.write(data["gene"])
    with b:
        st.markdown("**Chromosome**")
        st.write(data["chromosome"])
        st.markdown("**Examples of antibodies**")
        st.write(data["antibodies"])
    st.markdown("**Why it matters**")
    st.write(data["importance"])
    st.warning("This is a high-level learning summary, not a complete antigen catalogue or a method for predicting an individual's phenotype. Laboratory antigen typing and antibody identification are required for clinical use.")

with tabs[5]:
    st.subheader("Rare and unusual blood-group phenotypes")
    rare = [
        ("Bombay phenotype (Oh / hh)", "The H antigen is absent or greatly reduced due to FUT1-related biology. Because H is the precursor for A and B antigen expression on red cells, routine forward typing can be misleading. People with the classic Bombay phenotype can have anti-H and generally require red cells from a compatible Bombay-phenotype donor.", "ABO typing alone can miss this phenotype; specialist testing is required."),
        ("Rh-null phenotype", "A very rare phenotype in which Rh-system antigens are absent from red cells. It can be associated with red-cell membrane abnormalities and creates complex transfusion requirements.", "The term 'golden blood' is a popular nickname, not a clinical category."),
        ("Duffy-null phenotype", "A phenotype lacking Fyᵃ and Fyᵇ expression on red cells in common forms. It is associated with reduced susceptibility to Plasmodium vivax infection in many settings, but biological context and genotype matter.", "Do not infer an individual's infection risk or ancestry from this phenotype."),
        ("Para-Bombay phenotypes", "A group of related phenotypes with weak or variable H expression on red cells and/or substances in secretions. Serologic patterns can be complex.", "Requires specialist immunohematology investigation."),
    ]
    for title, description, caution in rare:
        with st.expander(title):
            st.write(description)
            st.caption(caution)
    st.info("Rare phenotype descriptions are for education. This app does not diagnose rare blood types or identify suitable donors.")

with tabs[6]:
    st.subheader("Knowledge check")
    questions = [
        {"q": "Which ABO phenotype has both A and B antigens on red cells?", "opts": ["O", "A", "B", "AB"], "a": "AB", "why": "AB red cells express both A and B antigens."},
        {"q": "Which blood type is commonly called the universal red-cell donor in the simplified ABO/RhD system?", "opts": ["AB+", "O−", "A+", "B−"], "a": "O−", "why": "O− red cells lack A, B and D antigens. Other antigens and clinical testing still matter."},
        {"q": "Can an RhD-negative person be assumed to have anti-D naturally?", "opts": ["Yes, always", "No", "Only if type O", "Only if type AB"], "a": "No", "why": "Anti-D is generally an immune antibody that can develop after exposure; it is not naturally present simply because someone is RhD-negative."},
        {"q": "Which gene is associated with the Duffy blood-group system?", "opts": ["ABO", "KEL", "ACKR1", "SLC14A1"], "a": "ACKR1", "why": "ACKR1 encodes the Duffy antigen receptor for chemokines."},
        {"q": "Why can't phenotype A alone tell us whether a parent is AA or AO?", "opts": ["Both genotypes can produce A phenotype", "A is recessive", "Rh controls ABO", "Phenotypes are random"], "a": "Both genotypes can produce A phenotype", "why": "A is expressed with either AA or AO genotype in the basic ABO model."},
        {"q": "What is required before a real red-cell transfusion?", "opts": ["This app's green result", "Only donor's ABO type", "Validated testing including antibody screen and crossmatch", "A population chart"], "a": "Validated testing including antibody screen and crossmatch", "why": "Clinical transfusion requires validated laboratory testing and professional oversight."},
    ]
    if "quiz_order" not in st.session_state:
        st.session_state.quiz_order = list(range(len(questions)))
        random.shuffle(st.session_state.quiz_order)
        st.session_state.quiz_submitted = False
    with st.form("knowledge_quiz"):
        answers = {}
        for idx, q_index in enumerate(st.session_state.quiz_order, start=1):
            q = questions[q_index]
            answers[q_index] = st.radio(f"{idx}. {q['q']}", q["opts"], key=f"quiz_{q_index}", index=None)
        submitted = st.form_submit_button("Check my answers")
    if submitted:
        st.session_state.quiz_answers = answers
        st.session_state.quiz_submitted = True
    if st.session_state.get("quiz_submitted"):
        submitted_answers = st.session_state.get("quiz_answers", {})
        score = sum(submitted_answers.get(i) == q["a"] for i, q in enumerate(questions))
        st.metric("Your score", f"{score} / {len(questions)}")
        for i in st.session_state.quiz_order:
            q = questions[i]
            correct = submitted_answers.get(i) == q["a"]
            st.markdown(f"**{'✓' if correct else '✕'} {q['q']}**")
            st.caption(f"Correct answer: {q['a']}. {q['why']}")
        if st.button("Try another quiz", key="new_quiz"):
            st.session_state.quiz_order = list(range(len(questions)))
            random.shuffle(st.session_state.quiz_order)
            st.session_state.quiz_submitted = False
            for i in range(len(questions)):
                st.session_state.pop(f"quiz_{i}", None)
            st.rerun()

with tabs[7]:
    st.subheader("Project scope and limitations")
    st.markdown("""
**Included**
- Simplified ABO/RhD red-cell compatibility reference.
- Eight-type donor-to-recipient matrix.
- ABO and RhD inheritance possibility explorer.
- Educational summaries of selected blood-group systems and rare phenotypes.
- Knowledge quiz with answer explanations.

**Not included**
- Actual laboratory blood typing, genotype determination or phenotype prediction.
- Antibody screening, antibody history or serologic crossmatching.
- Extended-antigen compatibility decisions or donor selection.
- Clinical risk scores, emergency-release decisions or patient-specific recommendations.
- Validated population-frequency estimates.

**Inheritance limitation:** A phenotype can correspond to more than one genotype. The simulator enumerates possibilities under a simplified Mendelian model and does not infer an individual genotype or assign phenotype-level probabilities.

**Clinical limitation:** A rule-compatible result is not proof that two blood samples are clinically compatible. Actual transfusion decisions require validated testing and qualified clinical oversight.
""")
    st.caption("HemaCheck is an educational software project, not a medical device or clinical decision-support system.")

st.markdown("---")
st.caption("HemaCheck · Educational blood-group biology explorer · Not for diagnosis, treatment or transfusion decisions")
