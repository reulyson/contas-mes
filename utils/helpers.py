from datetime import datetime

def calcular_totais(contas):
    if not contas:
        return 0.0, 0.0
    total = sum(c["valor"] for c in contas)
    pago = sum(c["valor"] for c in contas if c["pago"])
    return total, pago

def get_next_month(mes_ano):
    mes, ano = map(int, mes_ano.split('/'))
    if mes == 12:
        return f"01/{ano + 1}"
    else:
        return f"{mes + 1:02d}/{ano}"

def format_currency(value):
    return f"R$ {value:,.2f}"

def get_current_month_year():
    now = datetime.now()
    return f"{now.month:02d}/{now.year}"

def calcular_resumo_geral(mes_ano, dados):
    try:
        total_salarios = sum(u["salario"] for u in dados["usuarios"].values())
        
        total_despesas_ind = sum(
            calcular_totais(u["contas"].get(mes_ano, []))[0]
            for u in dados["usuarios"].values()
        )
        
        total_despesas_ger = calcular_totais(dados["despesas_gerais"].get(mes_ano, []))[0]
        
        return {
            "total_salarios": total_salarios,
            "total_despesas": total_despesas_ind + total_despesas_ger,
            "saldo_consolidado": (total_salarios - total_despesas_ind) - total_despesas_ger
        }
    except Exception as e:
        raise ValueError(f"Erro no cálculo: {str(e)}")