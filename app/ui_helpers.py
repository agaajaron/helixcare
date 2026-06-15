import json, re

import streamlit as st


def extract_json_block(text: str):
    m = re.findall(r"\{[\s\S]*\}$", text.strip())
    if not m:
        return None
    try:
        return json.loads(m[-1])
    except Exception:
        return None


def pill(text, color="#0ea5e9"):
    st.markdown(f"""
    <span style="display:inline-block;padding:4px 10px;border-radius:999px;background:{color}22;color:{color};border:1px solid {color}55;font-size:0.85rem;margin-right:6px;">{text}</span>
    """, unsafe_allow_html=True)
