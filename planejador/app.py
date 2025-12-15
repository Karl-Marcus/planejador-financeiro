# Bibliotecas
import streamlit as st
from financeiro import calcular_planejamento
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import tempfile
import matplotlib.pyplot as plt
from reportlab.platypus import Image
from io import BytesIO

if "resumo_cenarios" not in st.session_state:
    st.session_state.resumo_cenarios = []

if "meta" not in st.session_state:
    st.session_state.meta = 0.0

# Funções
def moeda_para_float(valor):
    try:
        return float(valor.replace(",","."))
    except:
        return 0.0

def interpretar_range(valor):
    # Se o campo estiver vazio ou só com espaços
    if not valor or valor.strip() == "":
        return 0.0, 0.0, 0.0

    valor = valor.replace(" ", "")

    try:
        if "a" in valor:
            minimo, maximo = valor.split("a")
            minimo = float(minimo.replace(",", "."))
            maximo = float(maximo.replace(",", "."))
            media = (minimo + maximo) / 2
            return minimo, media, maximo

        if "-" in valor:
            minimo, maximo = valor.split("-")
            minimo = float(minimo.replace(",", "."))
            maximo = float(maximo.replace(",", "."))
            media = (minimo + maximo) / 2
            return minimo, media, maximo

        # Valor único
        v = float(valor.replace(",", "."))
        return v, v, v

    except ValueError:
        # Caso o usuário digite algo inválido
        return 0.0, 0.0, 0.0

def gerar_grafico_cenarios(dfs_cenarios, meta):
    plt.figure(figsize=(8, 5))

    for nome, df in dfs_cenarios.items():
        plt.plot(df["Mês"], df["Reserva acumulada"], label=nome)

    plt.axhline(meta, linestyle="--", linewidth=2, label="Meta")
    plt.xlabel("Meses")
    plt.ylabel("Reserva acumulada (R$)")
    plt.title("Evolução da Reserva por Cenário")
    plt.legend()
    plt.grid(True)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", dpi=150)
    plt.close()

    buffer.seek(0)
    return buffer

def gerar_pdf(resumo_cenarios, dfs_cenarios, meta):
    arquivo_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        arquivo_temp.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("<b>Planejamento Financeiro – Comparativo de Cenários</b>", styles["Title"]))
    elementos.append(Paragraph(f"Meta financeira: R$ {meta:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), styles["Normal"]))
    elementos.append(Paragraph("<br/>", styles["Normal"]))

    # Cabeçalho da tabela
    dados_tabela = [["Cenário", "Meses para atingir a meta", "Reserva final (R$)"]]

    for c in resumo_cenarios:
        meses = c["Meses para atingir a meta"] or "Não atingida"
        reserva = f'R$ {c["Reserva final (R$)"]:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")
        dados_tabela.append([c["Cenário"], meses, reserva])

    tabela = Table(dados_tabela, hAlign="LEFT")
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("TOPPADDING", (0,0), (-1,0), 8),
    ]))

    elementos.append(tabela)
    
    elementos.append(Paragraph("<br/><b>Comparação visual dos cenários</b><br/>", styles["Normal"]))

    grafico_buffer = gerar_grafico_cenarios(dfs_cenarios, meta)
    imagem = Image(grafico_buffer, width=400, height=250)

    elementos.append(imagem)

    doc.build(elementos)

    return arquivo_temp.name

# Configurações dos inputs 
st.set_page_config(page_title="Planejador Financeiro", layout="centered")

st.title("💰 Planejador de Gastos Pessoal")
st.markdown("Planeje seus gastos e veja quando você atinge sua meta financeira.")

st.header("📥 Entradas")

renda_fixa_txt = st.text_input(
    "Renda fixa mensal (R$)",
    placeholder="Ex: 2500"
)

renda_variavel_txt = st.text_input(
    "Renda variável mensal (R$)",
    placeholder="Ex: 500 ou 600 a 1000"
)

gastos_fixos_txt = st.text_input(
    "Gastos fixos mensais (R$)",
    placeholder="Ex: 1800"
)

gastos_variaveis_txt = st.text_input(
    "Gastos variáveis mensais (R$)",
    placeholder="Ex: 300 ou 250 a 400"
)

meta_txt = st.text_input(
    "Meta financeira (R$)",
    placeholder="Ex: 5000"
)

renda_fixa = moeda_para_float(renda_fixa_txt)
renda_variavel = moeda_para_float(renda_variavel_txt)
gastos_fixos = moeda_para_float(gastos_fixos_txt)
gastos_variaveis = moeda_para_float(gastos_variaveis_txt)
meta = moeda_para_float(meta_txt)

renda_var_min, renda_var_media, renda_var_max = interpretar_range(renda_variavel_txt)
gasto_var_min, gasto_var_medio, gasto_var_max = interpretar_range(gastos_variaveis_txt)

# Botão
if st.button("📊 Calcular planejamento"):

    # validações
    if meta <= 0:
        st.error("⚠️ Informe uma meta financeira válida.")
        st.stop()

    if renda_fixa <= 0 and renda_var_media <= 0:
        st.error("⚠️ Informe pelo menos uma fonte de renda.")
        st.stop()

    if gastos_fixos <= 0 and gasto_var_medio <= 0:
        st.error("⚠️ Informe ao menos um tipo de gasto.")
        st.stop()

    cenarios = {
        "Pessimista": {
            "renda_variavel": renda_var_min,
            "gastos_variaveis": gasto_var_max
        },
        "Realista": {
            "renda_variavel": renda_var_media,
            "gastos_variaveis": gasto_var_medio
        },
        "Otimista": {
            "renda_variavel": renda_var_max,
            "gastos_variaveis": gasto_var_min
        }
    }

    st.session_state.dfs_cenarios = {}
    st.session_state.resumo_cenarios = []
    st.session_state.meta = meta

    for nome, valores in cenarios.items():
        st.subheader(f"📌 Cenário {nome}")

        df = calcular_planejamento(
            renda_fixa,
            valores["renda_variavel"],
            gastos_fixos,
            valores["gastos_variaveis"],
            meta
        )

        if df.empty:
            st.warning("Planejamento não pôde ser calculado.")
            continue

        st.session_state.dfs_cenarios[nome] = df.copy()
        st.dataframe(df, use_container_width=True)
        st.line_chart(df.set_index("Mês")["Reserva acumulada"])

        ultimo_mes = df.iloc[-1]

        if ultimo_mes["Reserva acumulada"] >= meta:
            meses = int(ultimo_mes["Mês"])
            st.success(f"🎯 Meta atingida em {meses} meses")
        else:
            meses = None
            st.warning("⚠️ Meta não atingida nesse cenário")

        st.session_state.resumo_cenarios.append({
            "Cenário": nome,
            "Meses para atingir a meta": meses,
            "Reserva final (R$)": round(ultimo_mes["Reserva acumulada"], 2)
        })

    # 🔹 TABELA FINAL
    st.divider()
    st.header("📊 Comparativo Final dos Cenários")
    st.dataframe(st.session_state.resumo_cenarios, use_container_width=True)
   
    # 🔹 GRÁFICO ÚNICO
    st.divider()
    st.header("📈 Comparação dos Cenários")

    df_grafico = None

    for nome, df in st.session_state.dfs_cenarios.items():
        temp = df[["Mês", "Reserva acumulada"]].copy()
        temp = temp.rename(columns={"Reserva acumulada": nome})

        if df_grafico is None:
            df_grafico = temp
        else:
            df_grafico = df_grafico.merge(temp, on="Mês", how="outer")

    df_grafico = df_grafico.set_index("Mês")
    st.line_chart(df_grafico)

st.divider()
st.subheader("📄 Exportar planejamento")

if st.session_state.resumo_cenarios:
    caminho_pdf = gerar_pdf(
        st.session_state.resumo_cenarios,
        st.session_state.dfs_cenarios,
        st.session_state.meta
    )

    with open(caminho_pdf, "rb") as f:
        st.download_button(
            label="⬇️ Baixar PDF",
            data=f,
            file_name="planejamento_financeiro.pdf",
            mime="application/pdf"
        )
else:
    st.info("ℹ️ Gere o planejamento antes de exportar o PDF.")