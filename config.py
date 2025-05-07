import streamlit as st

def setup_page_config():
    st.set_page_config(
        page_title="Controle Financeiro Mensal",
        layout="wide",
        page_icon="💰"
    )

def load_custom_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)