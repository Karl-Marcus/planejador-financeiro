import pandas as pd


def calcular_planejamento(
        renda_fixa,
        renda_variavel,
        gastos_fixos,
        gastos_variaveis,
        meta,
        meses_max=24
):
    dados = []
    reserva = 0

    for mes in range(1, meses_max +1):
        renda_total = renda_fixa + renda_variavel
        gastos_total = gastos_fixos + gastos_variaveis
        saldo = renda_total - gastos_total
        reserva += saldo

        dados.append({
            "Mês": mes,
            "Renda": renda_total,
            "Gastos": gastos_total,
            "Saldo do mês": saldo,
            "Reserva acumulada": reserva
        })

        if reserva >= meta:
            break

    return pd.DataFrame(dados)