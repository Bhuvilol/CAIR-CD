import streamlit as st
import sys
from pathlib import Path
from collections import Counter
import pandas as pd

# --------------------------------------------------
# Path setup
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from query_engine.task1_explainer import answer_query

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Pravaah – Conversational Causal Intelligence",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS (safe, lightweight)
# --------------------------------------------------
st.markdown("""
<style>
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 18px;
    margin: 4px 6px 4px 0;
    font-size: 0.85rem;
    color: white;
}
.outcome { background-color: #7c2d12; }
.factor { background-color: #0f766e; }
.card {
    background-color: #020617;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #1e293b;
}
.section {
    margin-top: 24px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title + subtitle
# --------------------------------------------------
st.title("🧠 Pravaah: Conversational Causal Intelligence")
st.caption(
    "Causal analysis • Evidence grounding • Multi-turn reasoning • Counterfactual prevention"
)

st.markdown("---")

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# 🔍 CAUSAL ANALYSIS
# --------------------------------------------------
st.header("🔍 Causal Analysis")

st.markdown(
    "Ask **why an outcome occurs** based on conversational behavior."
)

query = st.text_input(
    "Analytical question",
    value="Why do escalation events occur?"
)

if st.button("Run Analysis", use_container_width=True):
    with st.spinner("Analyzing conversations..."):
        analysis = answer_query(query)

    st.session_state["last_analysis"] = analysis
    st.session_state.chat_history = []
    st.session_state.pop("last_counterfactual", None)

# --------------------------------------------------
# DISPLAY ANALYSIS RESULTS
# --------------------------------------------------
if "last_analysis" in st.session_state:
    analysis = st.session_state["last_analysis"]

    st.markdown("### 🏷️ Outcome")
    st.markdown(
        f"<span class='badge outcome'>{analysis['outcome_event']}</span>",
        unsafe_allow_html=True
    )

    st.markdown("### 🧩 Causal Factors")
    for f in analysis.get("causal_factors", []):
        st.markdown(
            f"<span class='badge factor'>{f}</span>",
            unsafe_allow_html=True
        )

    st.markdown("### 🧠 Explanation")
    st.info(analysis["explanation"])

    st.markdown("### 📊 Key Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Causal Factors", len(analysis.get("causal_factors", [])))
    m2.metric("Evidence Spans", len(analysis.get("evidence", [])))
    m3.metric("Outcome Type", analysis["outcome_event"])

    col1, col2 = st.columns(2)

    # ---------------- ML PANEL ----------------
    with col1:
        st.markdown("### 🤖 ML Prediction")
        ml = analysis.get("ml_prediction")
        if ml:
            st.success(ml["predicted_label"])
            st.progress(min(ml["confidence"], 1.0))
            st.caption(f"Confidence: {ml['confidence']:.3f}")

            if ml["confidence"] > 0.8:
                st.success("High confidence prediction")
            elif ml["confidence"] > 0.5:
                st.warning("Moderate confidence prediction")
            else:
                st.error("Low confidence prediction")

    # ---------------- CHART PANEL ----------------
    with col2:
        st.markdown("### 📊 Causal Factor Distribution")
        counts = Counter(analysis.get("causal_factors", []))
        if counts:
            df = pd.DataFrame.from_dict(
                counts, orient="index", columns=["Frequency"]
            )
            st.bar_chart(df)

    # ---------------- EVIDENCE ----------------
    st.markdown("### 🧾 Evidence (Traceable)")
    for e in analysis.get("evidence", []):
        with st.expander(
            f"{e['conversation_id']} • {e['signal']}"
        ):
            st.write(f"Domain: {e['domain']}")
            st.write(f"Turn span: {e['turn_span']}")

    st.markdown("---")

    # --------------------------------------------------
    # 💬 FOLLOW-UP ANALYSIS (FIXED POSITION)
    # --------------------------------------------------
    st.header("💬 Follow-Up Reasoning")
    with st.expander("💡 Supported follow-up questions"):
        st.markdown("""
            You can ask analytical follow-ups such as:
            
            - **Which factor matters most?**
            - **How early does escalation appear?**
            - **Does this vary by domain?**
            - **Which signals dominate before the outcome?**
            - **What pattern repeats most frequently?**
            
            These questions are answered using **evidence-grounded causal analysis**.
            Questions outside this scope are intentionally restricted to avoid hallucination.
            """)


    with st.form("followup_form"):
        followup = st.text_input("Ask a follow-up question")
        ask = st.form_submit_button("Ask")

    if ask and followup:
        st.session_state.chat_history.append(
            {"role": "user", "content": followup}
        )

        with st.spinner("Reasoning..."):
            response = answer_query(followup)

        text = response.get("answer", response.get("explanation", ""))
        st.session_state.chat_history.append(
            {"role": "assistant", "content": text}
        )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown("---")

    # --------------------------------------------------
    # 🔁 COUNTERFACTUAL SIMULATOR (SELF-CONTAINED)
    # --------------------------------------------------
    st.header("🔁 Counterfactual Simulator")

    st.markdown(
        "Explore **what would have prevented this outcome** using identified causal factors."
    )

    if st.button("Generate Counterfactuals", use_container_width=True):
        with st.spinner("Simulating preventive interventions..."):
            cf = answer_query("What would have prevented this outcome?")
        st.session_state["last_counterfactual"] = cf

    if "last_counterfactual" in st.session_state:
        response = st.session_state["last_counterfactual"]

        for idx, item in enumerate(
            response.get("counterfactuals", []), 1
        ):
            with st.expander(
                f"Intervention {idx}: {item['target_factor']}"
            ):
                st.markdown(
                    f"""
                    **Target Factor:** `{item['target_factor']}`  
                    **Suggested Action:** {item['intervention']}  
                    **Expected Effect:** {item['estimated_effect']}
                    """
                )

        with st.expander("Raw counterfactual output (JSON)"):
            st.json(response)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Pravaah — Causal Analysis & Interactive Reasoning over Conversational Data | Hackathon Submission"
)
