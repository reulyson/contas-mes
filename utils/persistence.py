import streamlit as st
import json
import os

def initialize_data():
    if "dados" not in st.session_state:
        dados_carregados = carregar_dados()
        st.session_state.dados = dados_carregados if dados_carregados else {
            "usuarios": {
                "Reulyson": {"salario": 0.0, "contas": {}},
                "Vanessa": {"salario": 0.0, "contas": {}}
            },
            "despesas_gerais": {},
            "gastos_fixos": {}
        }

def carregar_dados():
    if os.path.exists('dados_financeiros.json'):
        with open('dados_financeiros.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def salvar_dados():
    with open('dados_financeiros.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.dados, f, ensure_ascii=False, indent=4)