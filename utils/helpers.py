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