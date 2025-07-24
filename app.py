
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ---------- Funções auxiliares ----------
def carregar_tarefas():
    if os.path.exists("tarefas_semanal.json"):
        with open("tarefas_semanal.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open("tarefas_semanal.json", "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def carregar_progresso():
    if os.path.exists("progresso.csv"):
        return pd.read_csv("progresso.csv")
    return pd.DataFrame(columns=["Data", "Meta", "Progresso (%)", "Observações"])

def salvar_progresso(df):
    df.to_csv("progresso.csv", index=False)

# ---------- Interface ----------
st.set_page_config(page_title="Painel da Stella", layout="wide")
st.sidebar.title("🌟 Painel Interativo")

# 🔁 ATUALIZEI AQUI COM TODAS AS ABAS
aba = st.sidebar.radio("Navegue pelas seções:", [
    "✅ Tarefas Semanais",
    "📊 Campanhas e Métricas",
    "🔑 Palavras-chave e Conversões",
    "📈 Performance da Campanha"
])

# ---------- Módulo 1 ----------
if aba == "✅ Tarefas Semanais":
    st.title("✅ Tarefas Semanais")
    tarefas = carregar_tarefas()

    st.subheader("📋 Lista de Tarefas")
    for i, tarefa in enumerate(tarefas):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.write(f"🔹 {tarefa}")
        with col2:
            if st.button("🗑️", key=f"del{i}"):
                tarefas.pop(i)
                salvar_tarefas(tarefas)
                st.experimental_rerun()

    st.subheader("➕ Adicionar nova tarefa")
    nova_tarefa = st.text_input("Descreva a tarefa:")
    if st.button("Adicionar tarefa"):
        if nova_tarefa.strip():
            tarefas.append(nova_tarefa.strip())
            salvar_tarefas(tarefas)
            st.success("Tarefa adicionada com sucesso!")
            st.experimental_rerun()

    st.subheader("📈 Registro de Progresso")
    progresso_df = carregar_progresso()
    st.dataframe(progresso_df)

    st.markdown("### ✏️ Atualizar progresso")
    with st.form("progresso_form"):
        data = st.date_input("Data")
        meta = st.text_input("Meta da semana")
        progresso = st.slider("Progresso (%)", 0, 100, 0)
        obs = st.text_area("Observações")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            novo_registro = {"Data": data, "Meta": meta, "Progresso (%)": progresso, "Observações": obs}
            progresso_df = progresso_df.append(novo_registro, ignore_index=True)
            salvar_progresso(progresso_df)
            st.success("Progresso registrado com sucesso!")
            st.experimental_rerun()

# ---------- Módulo 2 ----------
elif aba == "📊 Campanhas e Métricas":
    st.title("📊 Análise de Campanhas de Tráfego")

    try:
        df = pd.read_csv("modulo2_dados_processados.csv")
        st.subheader("📌 Visão Geral das Campanhas")
        st.dataframe(df)

        st.subheader("🔍 Análises")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Total Investido (R$)", round(df["Custo (R$)"].sum(), 2))
            st.metric("🛒 Total de Conversões", int(df["Conversões"].sum()))
        with col2:
            st.metric("📈 ROAS Médio", round(df["ROAS"].mean(), 2))
            st.metric("💵 CPC Médio Geral (R$)", round(df["CPC Médio (R$)"].mean(), 2))

        st.subheader("📉 Gráficos")
        st.bar_chart(df.set_index("Campanha")["ROAS"])
        st.bar_chart(df.set_index("Campanha")["Conversões"])

    except Exception as e:
        st.warning("⚠️ Não foi possível carregar os dados do Módulo 2.")
        st.text(str(e))

# ---------- Módulo 3 ----------
elif aba == "🔑 Palavras-chave e Conversões":
    st.title("🔑 Análise de Palavras-chave e Conversões")

    uploaded_file = st.file_uploader("📤 Envie o arquivo CSV com os termos de pesquisa", type=["csv"], key="upload_kw")

    if uploaded_file:
        try:
            df_kw = pd.read_csv(uploaded_file)
            st.subheader("📄 Visualização do Arquivo")
            st.dataframe(df_kw.head())

            if "Palavra-chave" in df_kw.columns and "Conversões" in df_kw.columns:
                st.subheader("🏆 Palavras com mais conversões")
                top = df_kw[["Palavra-chave", "Conversões"]].sort_values(by="Conversões", ascending=False)
                st.table(top.head(10))
                st.bar_chart(top.set_index("Palavra-chave"))
            else:
                st.warning("⚠️ O CSV deve conter as colunas 'Palavra-chave' e 'Conversões'.")

        except Exception as e:
            st.error("Erro ao processar o arquivo.")
            st.text(str(e))

# ---------- Módulo 4 ----------
elif aba == "📈 Performance da Campanha":
    st.title("📈 Performance Diária da Campanha")

    uploaded_perf = st.file_uploader("📤 Envie o arquivo de performance (CSV)", type=["csv"], key="upload_perf")

    if uploaded_perf:
        try:
            df_perf = pd.read_csv(uploaded_perf)

            st.subheader("📊 Visualização do Arquivo")
            st.dataframe(df_perf.head())

            colunas_esperadas = ["Data", "Custo", "Conversões", "Cliques", "Valor Conversão"]
            if all(col in df_perf.columns for col in colunas_esperadas):
                df_perf["Data"] = pd.to_datetime(df_perf["Data"])
                df_perf = df_perf.sort_values("Data")
                df_perf["CPC"] = df_perf["Custo"] / df_perf["Cliques"]
                df_perf["ROAS"] = df_perf["Valor Conversão"] / df_perf["Custo"]

                st.subheader("📌 Métricas por Dia")
                st.dataframe(df_perf[["Data", "Custo", "Cliques", "Conversões", "CPC", "ROAS"]])

                st.subheader("📉 Tendência Diária")
                st.line_chart(df_perf.set_index("Data")[["Custo", "Conversões", "CPC", "ROAS"]])
            else:
                st.warning("⚠️ Certifique-se de que o arquivo contenha: " + ", ".join(colunas_esperadas))
        except Exception as e:
            st.error("Erro ao processar o arquivo de performance.")
            st.text(str(e))
