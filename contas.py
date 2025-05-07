# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import json
import os
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Controle Financeiro Mensal",
    layout="wide",
    page_icon="💰"
)

# CSS personalizado com responsividade
st.markdown("""
<style>
    /* Estilos base */
    .metric-card {
        border-left: 4px solid #6a5acd;
        padding: 15px;
        border-radius: 8px;
        background-color: #fffaf0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .metric-card h3 {
        color: #4682b4;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    .metric-card p {
        font-size: 24px;
        margin: 0;
        font-weight: 600;
        color: #2f4f4f;
    }
    
    .positive { color: #008000; }
    .negative { color: #ff4500; }
    
    .stButton>button { width: 100%; }
    .stNumberInput>div>input { text-align: right; }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .metric-card {
            padding: 10px;
            margin-bottom: 15px;
        }
        
        .metric-card p {
            font-size: 20px;
        }
        
        .css-1v0mbdj {
            flex-direction: column;
        }
        
        .css-1v0mbdj > div {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Controle Financeiro Mensal")

# Funções de persistência
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

# Inicialização dos dados com persistência
if "dados" not in st.session_state:
    dados_carregados = carregar_dados()
    st.session_state.dados = dados_carregados if dados_carregados else {
        "usuarios": {
            "Usuário 1": {"salario": 0.0, "contas": {}},
            "Usuário 2": {"salario": 0.0, "contas": {}}
        },
        "despesas_gerais": {}
    }

# Funções auxiliares
def adicionar_conta(tipo, usuario=None, mes_ano=None):
    target = st.session_state.dados["despesas_gerais"] if tipo == "geral" else st.session_state.dados["usuarios"][usuario]["contas"]
    if mes_ano not in target:
        target[mes_ano] = []
    target[mes_ano].append({
        "descricao": "",
        "valor": 0.0,
        "pago": False,
        "responsavel": usuario if tipo == "individual" else "Todos"
    })
    salvar_dados()

def excluir_conta(tipo, usuario=None, mes_ano=None, index=None):
    target = st.session_state.dados["despesas_gerais"] if tipo == "geral" else st.session_state.dados["usuarios"][usuario]["contas"]
    target[mes_ano].pop(index)
    salvar_dados()
    st.rerun()

def calcular_totais(contas):
    if not contas:
        return 0.0, 0.0
    total = sum(c["valor"] for c in contas)
    pago = sum(c["valor"] for c in contas if c["pago"])
    return total, pago

# Barra lateral
with st.sidebar:
    st.header("🔧 Configurações")
    mes_atual = st.selectbox("Mês", range(1, 13), index=datetime.now().month - 1, 
                            format_func=lambda x: datetime(1900, x, 1).strftime('%B'))
    ano_atual = st.selectbox("Ano", range(2020, 2031), index=datetime.now().year - 2020)
    mes_ano = f"{mes_atual:02d}/{ano_atual}"
    st.markdown("---")
    st.markdown("### Ações Rápidas")
    if st.button("➕ Nova Despesa Geral"):
        adicionar_conta("geral", None, mes_ano)
    
    st.markdown("---")
    st.markdown("### Backup")
    if st.button("💾 Fazer Backup dos Dados"):
        with open('backup_financeiro.json', 'w', encoding='utf-8') as f:
            json.dump(st.session_state.dados, f, ensure_ascii=False, indent=4)
        st.success("Backup salvo como 'backup_financeiro.json'")

# Layout principal
tab_ind, tab_geral, tab_resumo = st.tabs(["👥 Despesas Individuais", "🏠 Despesas Gerais", "📊 Resumo Avançado"])

with tab_ind:
    col1, col2 = st.columns(2, gap="large")
    usuarios = list(st.session_state.dados["usuarios"].keys())

    for i, usuario in enumerate(usuarios):
        with col1 if i == 0 else col2:
            with st.expander(f"### 👤 {usuario}", expanded=True):
                # Seção de Salário
                st.markdown("#### 💰 Salário")
                novo_salario = st.number_input(
                    f"Valor do salário", 
                    value=st.session_state.dados["usuarios"][usuario]["salario"],
                    key=f"sal_{usuario}",
                    format="%.2f"
                )
                
                if novo_salario != st.session_state.dados["usuarios"][usuario]["salario"]:
                    st.session_state.dados["usuarios"][usuario]["salario"] = novo_salario
                    salvar_dados()
                
                # Seção de Despesas
                st.markdown("#### 📝 Despesas")
                st.button(f"Adicionar nova despesa", 
                         on_click=adicionar_conta, 
                         args=("individual", usuario, mes_ano),
                         key=f"btn_add_{usuario}")

                contas = st.session_state.dados["usuarios"][usuario]["contas"].get(mes_ano, [])
                for idx, conta in enumerate(contas):
                    with st.container():
                        cols = st.columns([4, 2, 1.5, 1])
                        with cols[0]:
                            nova_descricao = st.text_input(
                                "Descrição", 
                                value=conta["descricao"],
                                key=f"ind_desc_{usuario}_{mes_ano}_{idx}",
                                label_visibility="collapsed",
                                placeholder="Descrição da despesa"
                            )
                            if nova_descricao != conta["descricao"]:
                                conta["descricao"] = nova_descricao
                                salvar_dados()
                                
                        with cols[1]:
                            novo_valor = st.number_input(
                                "Valor", 
                                value=conta["valor"], 
                                step=0.01,
                                key=f"ind_val_{usuario}_{mes_ano}_{idx}",
                                label_visibility="collapsed",
                                format="%.2f"
                            )
                            if novo_valor != conta["valor"]:
                                conta["valor"] = novo_valor
                                salvar_dados()
                                
                        with cols[2]:
                            pago = st.checkbox(
                                "Pago", 
                                value=conta["pago"],
                                key=f"ind_pago_{usuario}_{mes_ano}_{idx}",
                                label_visibility="collapsed"
                            )
                            if pago != conta["pago"]:
                                conta["pago"] = pago
                                salvar_dados()
                                
                        with cols[3]:
                            if st.button("🗑️", key=f"ind_del_{usuario}_{mes_ano}_{idx}"):
                                excluir_conta("individual", usuario, mes_ano, idx)

                # Resumo Individual
                salario = st.session_state.dados["usuarios"][usuario]["salario"]
                total, pago = calcular_totais(contas)
                pendente = total - pago
                saldo = salario - total
                saldo_class = "positive" if saldo >= 0 else "negative"
                
                st.markdown("---")
                st.markdown("### 📊 Resumo Individual")
                
                with st.container():
                    col_res1, col_res2, col_res3 = st.columns(3)
                    with col_res1:
                        st.markdown(f"**Total Despesas**  \nR$ {total:,.2f}")
                    with col_res2:
                        st.markdown(f"**Pago**  \nR$ {pago:,.2f}")
                    with col_res3:
                        st.markdown(f"**Pendente**  \nR$ {pendente:,.2f}")
                    
                    st.markdown(f"**Saldo**  \n<span class='{saldo_class}'>R$ {saldo:,.2f}</span>", 
                               unsafe_allow_html=True,
                               help="Salário menos todas as despesas (pagas e não pagas)")

with tab_geral:
    with st.expander("### 🏠 Despesas Gerais", expanded=True):
        st.button("➕ Adicionar Nova Despesa Geral",
                 on_click=adicionar_conta,
                 args=("geral", None, mes_ano),
                 key="btn_add_geral")

        despesas = st.session_state.dados["despesas_gerais"].get(mes_ano, [])
        for idx, despesa in enumerate(despesas):
            with st.container():
                cols = st.columns([4, 2, 1.5, 1])
                with cols[0]:
                    nova_descricao = st.text_input(
                        "Descrição", 
                        value=despesa["descricao"],
                        key=f"ger_desc_{mes_ano}_{idx}",
                        label_visibility="collapsed",
                        placeholder="Descrição da despesa"
                    )
                    if nova_descricao != despesa["descricao"]:
                        despesa["descricao"] = nova_descricao
                        salvar_dados()
                        
                with cols[1]:
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
                        
                with cols[2]:
                    pago = st.checkbox(
                        "Pago", 
                        value=despesa["pago"],
                        key=f"ger_pago_{mes_ano}_{idx}",
                        label_visibility="collapsed"
                    )
                    if pago != despesa["pago"]:
                        despesa["pago"] = pago
                        salvar_dados()
                        
                with cols[3]:
                    if st.button("🗑️", key=f"ger_del_{mes_ano}_{idx}"):
                        excluir_conta("geral", None, mes_ano, idx)

        # Resumo Geral
        total_geral, pago_geral = calcular_totais(despesas)
        pendente_geral = total_geral - pago_geral
        
        st.markdown("---")
        st.markdown("### 📊 Resumo Geral")
        
        with st.container():
            col_ger1, col_ger2, col_ger3 = st.columns(3)
            with col_ger1:
                st.markdown(f"**Total Despesas**  \nR$ {total_geral:,.2f}")
            with col_ger2:
                st.markdown(f"**Pago**  \nR$ {pago_geral:,.2f}")
            with col_ger3:
                st.markdown(f"**Pendente**  \nR$ {pendente_geral:,.2f}")

with tab_resumo:
    st.markdown("## 📈 Visualizações Avançadas")
    
    # Gráfico de distribuição de despesas
    st.markdown("### 📊 Distribuição de Despesas")
    
    dados_grafico = []
    for usuario, info in st.session_state.dados["usuarios"].items():
        contas = info["contas"].get(mes_ano, [])
        for conta in contas:
            dados_grafico.append({
                "Tipo": "Individual",
                "Responsável": usuario,
                "Descrição": conta["descricao"],
                "Valor": conta["valor"],
                "Pago": "Sim" if conta["pago"] else "Não"
            })
    
    for conta in st.session_state.dados["despesas_gerais"].get(mes_ano, []):
        dados_grafico.append({
            "Tipo": "Geral",
            "Responsável": "Todos",
            "Descrição": conta["descricao"],
            "Valor": conta["valor"],
            "Pago": "Sim" if conta["pago"] else "Não"
        })
    
    if dados_grafico:
        df = pd.DataFrame(dados_grafico)
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(df, names='Tipo', values='Valor', title='Proporção Individual vs Geral')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='Responsável', y='Valor', color='Pago', 
                        title='Despesas por Responsável')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhuma despesa cadastrada para este mês.")

# Resumo Consolidado
st.markdown("---")
st.markdown("## 📈 Resumo Consolidado")

total_salarios = sum(u["salario"] for u in st.session_state.dados["usuarios"].values())
total_despesas_ind = sum(
    calcular_totais(u["contas"].get(mes_ano, []))[0]
    for u in st.session_state.dados["usuarios"].values()
)
total_despesas_ger = calcular_totais(st.session_state.dados["despesas_gerais"].get(mes_ano, []))[0]
total_despesas = total_despesas_ind + total_despesas_ger
saldo_total = total_salarios - total_despesas
saldo_class = "positive" if saldo_total >= 0 else "negative"

# Criando métricas estilizadas
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Salários</h3>
        <p>R$ {total_salarios:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Despesas</h3>
        <p>R$ {total_despesas:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Saldo Total</h3>
        <p class="{saldo_class}">R$ {saldo_total:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)