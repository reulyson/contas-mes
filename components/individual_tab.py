import streamlit as st
from utils.helpers import calcular_totais
from utils.persistence import salvar_dados

def render_individual_tab(mes_ano):
    col1, col2 = st.columns(2, gap="large")
    usuarios = list(st.session_state.dados["usuarios"].keys())

    for i, usuario in enumerate(usuarios):
        with col1 if i == 0 else col2:
            render_usuario_section(usuario, mes_ano)

def render_usuario_section(usuario, mes_ano):
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
        render_expense_form(usuario, mes_ano)
        render_expense_list(usuario, mes_ano)
        render_user_summary(usuario, mes_ano)

def render_expense_form(usuario, mes_ano):
    with st.form(f"form_despesa_{usuario}", clear_on_submit=True):
        descricao = st.text_input("Descrição da despesa", key=f"desc_{usuario}")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f", key=f"val_{usuario}")
        repetir = st.checkbox("Repetir no próximo mês", key=f"rep_{usuario}")
        
        if st.form_submit_button("➕ Adicionar Despesa"):
            if descricao and valor:
                adicionar_conta_individual(usuario, mes_ano, descricao, float(valor), repetir)
                st.rerun()

def adicionar_conta_individual(usuario, mes_ano, descricao, valor, repetir):
    if mes_ano not in st.session_state.dados["usuarios"][usuario]["contas"]:
        st.session_state.dados["usuarios"][usuario]["contas"][mes_ano] = []
    
    st.session_state.dados["usuarios"][usuario]["contas"][mes_ano].append({
        "descricao": descricao,
        "valor": valor,
        "pago": False,
        "repetir": repetir,
        "responsavel": usuario
    })
    salvar_dados()

def render_expense_list(usuario, mes_ano):
    contas = st.session_state.dados["usuarios"][usuario]["contas"].get(mes_ano, [])
    
    if not contas:
        st.info("Nenhuma despesa cadastrada para este mês.")
        return
    
    for idx, conta in enumerate(contas):
        with st.container():
            cols = st.columns([1.5, 4, 2, 1.5, 1])
            with cols[0]:
                repetir = st.checkbox(
                    "Repetir", 
                    value=conta.get("repetir", False),
                    key=f"ind_repetir_{usuario}_{mes_ano}_{idx}",
                )
                if repetir != conta.get("repetir", False):
                    conta["repetir"] = repetir
                    salvar_dados()

            with cols[1]:
                nova_descricao = st.text_input(
                    "Descrição", 
                    value=conta["descricao"],
                    key=f"ind_desc_{usuario}_{mes_ano}_{idx}",
                    label_visibility="collapsed"
                )
                if nova_descricao != conta["descricao"]:
                    conta["descricao"] = nova_descricao
                    salvar_dados()
                    
            with cols[2]:
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
                    
            with cols[3]:
                pago = st.checkbox(
                    "Pago", 
                    value=conta["pago"],
                    key=f"ind_pago_{usuario}_{mes_ano}_{idx}",
                )
                if pago != conta["pago"]:
                    conta["pago"] = pago
                    salvar_dados()
                    
            with cols[4]:
                if st.button("🗑️", key=f"ind_del_{usuario}_{mes_ano}_{idx}"):
                    excluir_conta_individual(usuario, mes_ano, idx)

def excluir_conta_individual(usuario, mes_ano, index):
    st.session_state.dados["usuarios"][usuario]["contas"][mes_ano].pop(index)
    salvar_dados()
    st.rerun()

def render_user_summary(usuario, mes_ano):
    salario = st.session_state.dados["usuarios"][usuario]["salario"]
    contas = st.session_state.dados["usuarios"][usuario]["contas"].get(mes_ano, [])
    total, pago = calcular_totais(contas)
    pendente = total - pago
    saldo = salario - total
    
    st.markdown("---")
    st.markdown("### 📊 Resumo Individual")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Despesas", f"R$ {total:,.2f}")
    with col2:
        st.metric("Pago", f"R$ {pago:,.2f}")
    with col3:
        st.metric("Pendente", f"R$ {pendente:,.2f}")
    
    st.metric("Saldo",
              f"R$ {saldo:,.2f}",
            )
    