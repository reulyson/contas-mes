import streamlit as st
from utils.helpers import calcular_resumo_geral

def render_consolidated_summary(mes_ano):
    try:
        resumo = calcular_resumo_geral(mes_ano, st.session_state.dados)
        
        st.markdown("## 📊 Resumo Consolidado")

        # Saldo Consolidado com Estilo Customizado
        saldo = resumo['saldo_consolidado']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Salários", f"R$ {resumo['total_salarios']:,.2f}")
            
        with col2:
            st.metric("Total Despesas", f"R$ {resumo['total_despesas']:,.2f}")
            
        with col3:
            st.metric("Saldo Consolidado", 
                      f"R$ {resumo['saldo_consolidado']:,.2f}",
                      delta=f"{resumo['saldo_consolidado']:+,.2f}" if resumo['saldo_consolidado'] != 0 else "0.00"
                      )
        
    except Exception as e:
        st.error(f"Erro ao calcular resumo: {str(e)}")
        st.warning("Verifique se há dados cadastrados para este mês")
    