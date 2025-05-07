import streamlit as st
from utils.persistence import salvar_dados

def render_fixed_costs_tab():
    st.markdown("## 📌 Gastos Fixos Mensais")
    st.info("ℹ️ Esta seção é apenas para registro informativo e não afeta os cálculos das outras abas.")
    
    render_fixed_cost_form()
    render_fixed_cost_list()

def render_fixed_cost_form():
    with st.form("form_gasto_fixo", clear_on_submit=True):
        descricao = st.text_input("Descrição do gasto fixo")
        valor = st.number_input("Valor mensal", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("➕ Adicionar Gasto Fixo"):
            if descricao and valor:
                st.session_state.dados["gastos_fixos"][descricao] = float(valor)
                salvar_dados()
                st.rerun()

def render_fixed_cost_list():
    st.markdown("### Seus Gastos Fixos")
    
    if not st.session_state.dados["gastos_fixos"]:
        st.warning("Nenhum gasto fixo cadastrado.")
    else:
        total = 0.0
        for descricao, valor in st.session_state.dados["gastos_fixos"].items():
            cols = st.columns([4, 2, 1])
            with cols[0]:
                st.markdown(f"**{descricao}**")
            with cols[1]:
                st.markdown(f"R$ {valor:,.2f}")
            with cols[2]:
                if st.button("🗑️", key=f"del_{descricao}"):
                    del st.session_state.dados["gastos_fixos"][descricao]
                    salvar_dados()
                    st.rerun()
            total += valor
        
        st.markdown("---")
        st.markdown(f"### 💰 Total de Gastos Fixos: R$ {total:,.2f}")