import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import calcular_totais

def render_summary_tab(mes_ano):
    st.markdown("## 📈 Visualizações Avançadas")
    
    # Gráfico de distribuição de despesas
    st.markdown("### 📊 Distribuição de Despesas")
    df = prepare_summary_data(mes_ano)
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(df, names='Tipo', values='Valor', 
                        title='Proporção Individual vs Geral',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='Responsável', y='Valor', color='Pago', 
                        title='Despesas por Responsável',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico para despesas que se repetem
        st.markdown("### 🔄 Despesas Recorrentes")
        fig = px.pie(df, names='Repetir', values='Valor', 
                    title='Proporção de Despesas que se Repetem',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📋 Detalhamento Completo")
        st.dataframe(df.sort_values('Valor', ascending=False), use_container_width=True)
    else:
        st.warning("Nenhuma despesa cadastrada para este mês.")

def prepare_summary_data(mes_ano):
    dados_grafico = []
    
    # Despesas individuais
    for usuario, info in st.session_state.dados["usuarios"].items():
        contas = info["contas"].get(mes_ano, [])
        for conta in contas:
            dados_grafico.append({
                "Tipo": "Individual",
                "Responsável": usuario,
                "Descrição": conta["descricao"],
                "Valor": conta["valor"],
                "Pago": "Sim" if conta["pago"] else "Não",
                "Repetir": "Sim" if conta.get("repetir", False) else "Não"
            })
    
    # Despesas gerais
    for conta in st.session_state.dados["despesas_gerais"].get(mes_ano, []):
        dados_grafico.append({
            "Tipo": "Geral",
            "Responsável": "Todos",
            "Descrição": conta["descricao"],
            "Valor": conta["valor"],
            "Pago": "Sim" if conta["pago"] else "Não",
            "Repetir": "Sim" if conta.get("repetir", False) else "Não"
        })
    
    return pd.DataFrame(dados_grafico) if dados_grafico else pd.DataFrame()