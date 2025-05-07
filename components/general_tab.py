import streamlit as st
from utils.helpers import calcular_totais
from utils.persistence import salvar_dados

def render_general_tab(mes_ano):
    with st.expander("### 🏠 Despesas Gerais", expanded=True):
        render_general_expense_form(mes_ano)
        render_general_expense_list(mes_ano)
        render_general_summary(mes_ano)

def render_general_expense_form(mes_ano):
    with st.form("form_despesa_geral", clear_on_submit=True):
        descricao = st.text_input("Descrição da despesa geral")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        repetir = st.checkbox("Repetir no próximo mês")
        
        if st.form_submit_button("➕ Adicionar Despesa Geral"):
            if descricao and valor:
                adicionar_conta_geral(mes_ano, descricao, float(valor), repetir)
                st.rerun()

def adicionar_conta_geral(mes_ano, descricao, valor, repetir):
    if mes_ano not in st.session_state.dados["despesas_gerais"]:
        st.session_state.dados["despesas_gerais"][mes_ano] = []
    
    st.session_state.dados["despesas_gerais"][mes_ano].append({
        "descricao": descricao,
        "valor": valor,
        "pago": False,
        "repetir": repetir,
        "responsavel": "Todos"
    })
    salvar_dados()

def render_general_expense_list(mes_ano):
    despesas = st.session_state.dados["despesas_gerais"].get(mes_ano, [])
    
    if not despesas:
        st.info("Nenhuma despesa geral cadastrada para este mês.")
        return
    
    for idx, despesa in enumerate(despesas):
        with st.container():
            cols = st.columns([1.5, 4, 2, 1.5, 1])
            with cols[0]:
                repetir = st.checkbox(
                    "Repetir", 
                    value=despesa.get("repetir", False),
                    key=f"ger_repetir_{mes_ano}_{idx}",
                )
                if repetir != despesa.get("repetir", False):
                    despesa["repetir"] = repetir
                    salvar_dados()
            with cols[1]:
                nova_descricao = st.text_input(
                    "Descrição", 
                    value=despesa["descricao"],
                    key=f"ger_desc_{mes_ano}_{idx}",
                    label_visibility="collapsed"
                )
                if nova_descricao != despesa["descricao"]:
                    despesa["descricao"] = nova_descricao
                    salvar_dados()
                    
            with cols[2]:
                novo_valor = st.number_input(
                    "Valor", 
                    value=despesa["valor"], 
                    step=0.01,
                    key=f"ger_val_{mes_ano}_{idx}",
                    label_visibility="collapsed",
                    format="%.2f"
                )
                if novo_valor != despesa["valor"]:
                    despesa["valor"] = novo_valor
                    salvar_dados()
                    
            with cols[3]:
                pago = st.checkbox(
                    "Pago", 
                    value=despesa["pago"],
                    key=f"ger_pago_{mes_ano}_{idx}",
                )
                if pago != despesa["pago"]:
                    despesa["pago"] = pago
                    salvar_dados()
                    
            with cols[4]:
                if st.button("🗑️", key=f"ger_del_{mes_ano}_{idx}"):
                    excluir_conta_geral(mes_ano, idx)

def excluir_conta_geral(mes_ano, index):
    st.session_state.dados["despesas_gerais"][mes_ano].pop(index)
    salvar_dados()
    st.rerun()

def render_general_summary(mes_ano):
    despesas = st.session_state.dados["despesas_gerais"].get(mes_ano, [])
    total_geral, pago_geral = calcular_totais(despesas)
    pendente_geral = total_geral - pago_geral
    
    st.markdown("---")
    st.markdown("### 📊 Resumo Geral")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Despesas Gerais", f"R$ {total_geral:,.2f}")
    with col2:
        st.metric("Pago", f"R$ {pago_geral:,.2f}")
    with col3:
        st.metric("Pendente", f"R$ {pendente_geral:,.2f}")