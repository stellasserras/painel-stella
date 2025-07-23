
import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Carrega as tarefas da semana
with open("tarefas_semanal.json", "r", encoding="utf-8") as f:
    tarefas = json.load(f)

# Dia atual
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
hoje = dias_semana[datetime.now().weekday()]

st.title("📌 Painel Empreendedora Stella")
st.subheader(f"Tarefas para hoje ({hoje})")

# Exibe as tarefas do dia
tarefas_hoje = tarefas.get(hoje, [])
tarefas_concluidas = st.multiselect("Marque as tarefas que você concluiu hoje:", tarefas_hoje)

# Salvar progresso
if st.button("✅ Salvar progresso"):
    if tarefas_concluidas:
        df = pd.read_csv("progresso.csv")
        data_atual = datetime.now().strftime("%Y-%m-%d")
        for tarefa in tarefas_concluidas:
            df = pd.concat([df, pd.DataFrame([[data_atual, hoje, tarefa]], columns=["Data", "Dia", "Tarefa"])], ignore_index=True)
        df.to_csv("progresso.csv", index=False)
        st.success("Progresso salvo com sucesso!")
    else:
        st.warning("Selecione pelo menos uma tarefa para salvar.")

# Mostrar relatório semanal
st.subheader("📈 Relatório da Semana")
df = pd.read_csv("progresso.csv")
df["Data"] = pd.to_datetime(df["Data"])
ultima_semana = df[df["Data"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
relatorio = ultima_semana.groupby(["Dia", "Tarefa"]).size().reset_index(name="Vezes Concluída")

st.dataframe(relatorio)
