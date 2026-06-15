import streamlit as st

CUSTOM_CSS = """
<style>
.card { background: #0b132b0d; border: 1px solid #ffffff22; border-radius: 16px; padding: 16px 18px; margin-bottom: 12px; }
.small { font-size: 0.88rem; opacity: 0.85; }
.kv { display:flex; gap:8px; flex-wrap:wrap; }
</style>
"""


def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
