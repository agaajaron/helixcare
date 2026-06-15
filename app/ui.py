import re, time
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from app.orchestrator import run_mri_pa_flow
from app.metrics import ensure_metrics_server
from app.llm import get_llm
from app.ui_helpers import extract_json_block, pill
from app.ui_styles import inject_custom_css

st.set_page_config(page_title="CareGraph • LlamaIndex Multi‑Agent RAG", page_icon="🩺", layout="wide")
ensure_metrics_server()
_llm = get_llm()

inject_custom_css()

st.title("CareGraph — Multi‑Agent Healthcare RAG (LlamaIndex)")
st.caption("Synthetic demo • Not for clinical use")

with st.sidebar:
    st.subheader("Settings")
    st.write("**LLM backend**")
    st.code(str(_llm)[:220] + ("..." if len(str(_llm))>220 else ""), language="text")
    st.write("**Tips**")
    st.markdown("- Use Member **M123** for seeded coverage\n- Try symptom: *low back pain*")

col1, col2, col3, col4 = st.columns([1.2,1,1,1])
with col1:
    member_id = st.text_input("Member ID", value="M123")
with col2:
    modality = st.selectbox("Modality", ["MRI","CT","X‑ray"], index=0)
with col3:
    symptom = st.text_input("Symptom", value="low back pain")
with col4:
    zip_code = st.text_input("ZIP", value="80301")

go = st.button("▶ Run Prior‑Auth Flow", type="primary", use_container_width=True)

if go:
    t0 = time.time()
    with st.spinner("Running agents and retrieval…"):
        raw = run_mri_pa_flow(member_id, modality, symptom, zip_code)
    dt = time.time() - t0

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Result")
    st.write(raw.split("{")[0].strip() or raw)

    st.markdown('<div class="kv">', unsafe_allow_html=True)
    pill(f"Latency ~ {dt:.2f}s")
    pill(f"Member: {member_id}", "#22c55e")
    pill(f"Plan: auto-detected", "#a855f7")
    pill(f"Modality: {modality}", "#f59e0b")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧾 Why Card", "📚 Source Snippets", "🪪 Raw Output"])

    with tab1:
        why = extract_json_block(raw)
        if why is None:
            st.warning("Could not parse structured Why Card JSON from the output.")
        else:
            st.json(why)

    with tab2:
        quotes = re.findall(r"“([^”]{10,400})”|\"([^\"\\n]{10,400})\"", raw)
        snippets = [q[0] or q[1] for q in quotes]
        if snippets:
            for q in snippets[:8]:
                st.markdown(f'> {q}')
                st.markdown('---')
        else:
            st.info("No explicit quotes detected. Ensure your policies include identifiable text to quote.")

    with tab3:
        st.code(raw, language="markdown")
else:
    st.info("Fill inputs and click **Run Prior‑Auth Flow** to see the multi‑agent pipeline in action.")
