import streamlit as st
from config import setup_page_config, load_custom_css
from components.sidebar import render_sidebar
from components.individual_tab import render_individual_tab
from components.general_tab import render_general_tab
from components.summary_tab import render_summary_tab
from components.fixed_costs_tab import render_fixed_costs_tab
from components.consolidated_summary import render_consolidated_summary
from utils.persistence import initialize_data

def main():
    # Configuração inicial
    setup_page_config()
    load_custom_css()
    initialize_data()
    
    st.title("📊 Controle Financeiro Mensal")
    
    # Barra lateral e seleção de mês/ano
    mes_ano = render_sidebar()
    
    # Abas principais
    tab_ind, tab_geral, tab_resumo, tab_fixos = st.tabs([
        "👥 Despesas Individuais", 
        "🏠 Despesas Gerais", 
        "📊 Resumo Avançado", 
        "📌 Gastos Fixos"
    ])
    
    with tab_ind:
        render_individual_tab(mes_ano)
    
    with tab_geral:
        render_general_tab(mes_ano)
    
    with tab_resumo:
        render_summary_tab(mes_ano)
    
    with tab_fixos:
        render_fixed_costs_tab()
    
    # Resumo Consolidado (adicionado após as abas)
    st.markdown("---")
    render_consolidated_summary(mes_ano)

if __name__ == "__main__":
    main()