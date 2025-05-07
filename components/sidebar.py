import streamlit as st
from datetime import datetime
from utils.helpers import get_next_month
from utils.persistence import salvar_dados

def render_sidebar():
    st.header("🔧 Configurações")
    
    # Seleção de mês/ano
    mes_atual = st.selectbox(
        "Mês", 
        range(1, 13), 
        index=datetime.now().month - 1,
        format_func=lambda x: datetime(1900, x, 1).strftime('%B')
    )
    ano_atual = st.selectbox(
        "Ano", 
        range(2020, 2031), 
        index=datetime.now().year - 2020
    )
    mes_ano = f"{mes_atual:02d}/{ano_atual}"
    
    # Copiar despesas repetidas se o mês foi alterado
    handle_month_change(mes_ano)
    
    return mes_ano

def handle_month_change(mes_ano):
    if "ultimo_mes" not in st.session_state:
        st.session_state.ultimo_mes = mes_ano
    elif st.session_state.ultimo_mes != mes_ano:
        copiar_despesas_repetidas(st.session_state.ultimo_mes)
        st.session_state.ultimo_mes = mes_ano

def copiar_despesas_repetidas(mes_atual):
    # Para despesas individuais
    for usuario, info in st.session_state.dados["usuarios"].items():
        if mes_atual in info["contas"]:
            despesas_repetir = [d for d in info["contas"][mes_atual] if d.get("repetir", False)]
            if despesas_repetir:
                mes_proximo = get_next_month(mes_atual)
                if mes_proximo not in info["contas"]:
                    info["contas"][mes_proximo] = []
                
                for despesa in despesas_repetir:
                    if not any(d["descricao"] == despesa["descricao"] for d in info["contas"][mes_proximo]):
                        info["contas"][mes_proximo].append({
                            "descricao": despesa["descricao"],
                            "valor": despesa["valor"],
                            "pago": False,
                            "repetir": True,
                            "responsavel": usuario
                        })
    
    # Para despesas gerais
    if mes_atual in st.session_state.dados["despesas_gerais"]:
        despesas_repetir = [d for d in st.session_state.dados["despesas_gerais"][mes_atual] if d.get("repetir", False)]
        if despesas_repetir:
            mes_proximo = get_next_month(mes_atual)
            if mes_proximo not in st.session_state.dados["despesas_gerais"]:
                st.session_state.dados["despesas_gerais"][mes_proximo] = []
            
            for despesa in despesas_repetir:
                if not any(d["descricao"] == despesa["descricao"] for d in st.session_state.dados["despesas_gerais"][mes_proximo]):
                    st.session_state.dados["despesas_gerais"][mes_proximo].append({
                        "descricao": despesa["descricao"],
                        "valor": despesa["valor"],
                        "pago": False,
                        "repetir": True,
                        "responsavel": "Todos"
                    })
    
    salvar_dados()