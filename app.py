
import streamlit as st
import pandas as pd
import datetime

# --- MÓDULO 1: TAREFAS E PROGRESSO ---
st.set_page_config(page_title="Painel Empreendedora Stella", layout="wide")

aba = st.sidebar.radio("📌 Selecione o Módulo:", ["✅ Tarefas Semanais", "📊 Campanhas e Métricas"])

if aba == "✅ Tarefas Semanais":
    st.title("✅ Painel de Tarefas Semanais")

    tarefas_file = "tarefas_semanal.json"
    progresso_file = "progresso.csv"

    try:
        tarefas = pd.read_json(tarefas_file)
    except:
        tarefas = pd.DataFrame(columns=["Tarefa", "Prazo"])

    try:
        progresso = pd.read_csv(progresso_file)
    except:
        progresso = pd.DataFrame(columns=["Tarefa", "Data Conclusão"])

    with st.form("nova_tarefa"):
        st.subheader("➕ Adicionar nova tarefa")
        nova_tarefa = st.text_input("Descrição da tarefa:")
        prazo = st.date_input("Prazo", datetime.date.today())
        submitted = st.form_submit_button("Adicionar")

        if submitted and nova_tarefa:
            tarefas = tarefas._append({"Tarefa": nova_tarefa, "Prazo": prazo}, ignore_index=True)
            tarefas.to_json(tarefas_file)
            st.success("Tarefa adicionada com sucesso!")

    st.subheader("📋 Tarefas Pendentes")
    if not tarefas.empty:
        for i, row in tarefas.iterrows():
            col1, col2 = st.columns([6, 1])
            col1.markdown(f"**{row['Tarefa']}** (até {row['Prazo']})")
            if col2.button("Concluir", key=f"done_{i}"):
                progresso = progresso._append({
                    "Tarefa": row["Tarefa"],
                    "Data Conclusão": datetime.date.today()
                }, ignore_index=True)
                progresso.to_csv(progresso_file, index=False)
                tarefas = tarefas.drop(index=i).reset_index(drop=True)
                tarefas.to_json(tarefas_file)
                st.experimental_rerun()
    else:
        st.info("Nenhuma tarefa pendente.")

    st.subheader("📈 Progresso")
    if not progresso.empty:
        st.dataframe(progresso)
    else:
        st.info("Você ainda não concluiu nenhuma tarefa.")

# --- MÓDULO 2: CAMPANHAS E MÉTRICAS ---
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
        st.warning("Não foi possível carregar os dados do Módulo 2.")
        st.text(str(e))
