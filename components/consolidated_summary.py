import streamlit as st
from utils.helpers import calcular_resumo_geral

def render_consolidated_summary(mes_ano):
    resumo = calcular_resumo_geral(mes_ano, st.session_state.dados)
    
    # Layout em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Salários")
        st.metric(
            label="Total", 
            value=f"R$ {resumo['total_salarios']:,.2f}",
            help="Soma de todos os salários cadastrados"
        )
        
    with col2:
        st.markdown("### 🛒 Despesas")
        st.metric(
            label="Individuais", 
            value=f"R$ {resumo['total_despesas_ind']:,.2f}"
        )
        st.metric(
            label="Gerais", 
            value=f"R$ {resumo['total_despesas_ger']:,.2f}"
        )
        st.metric(
            label="Total", 
            value=f"R$ {resumo['total_despesas']:,.2f}",
            delta=f"R$ {resumo['total_despesas_ind'] + resumo['total_despesas_ger']:,.2f}",
            help="Soma de todas as despesas (individuais + gerais)"
        )
        
    with col3:
        st.markdown("### 📊 Saldos")
        st.metric(
            label="Individual Total", 
            value=f"R$ {resumo['saldo_individual_total']:,.2f}",
            help="Soma dos salários menos despesas individuais"
        )
        st.metric(
            label="Consolidado", 
            value=f"R$ {resumo['saldo_consolidado']:,.2f}",
            delta_color="inverse" if resumo['saldo_consolidado'] < 0 else "normal",
            help="Saldo individual total menos despesas gerais"
        )
    
    # Gráfico de distribuição
    st.markdown("---")
    st.markdown("### 📈 Distribuição Financeira")
    
    dados_grafico = {
        "Categoria": ["Salários", "Despesas Individuais", "Despesas Gerais"],
        "Valor": [
            resumo['total_salarios'],
            resumo['total_despesas_ind'],
            resumo['total_despesas_ger']
        ]
    }
    
    st.bar_chart(
        data=dados_grafico,
        x="Categoria",
        y="Valor",
        color="#4CAF50"  # Cor verde
    )