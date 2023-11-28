import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd

def dashboard():
    st.title("📈 Dashboard")

    df = st.session_state.df

    fig = px.bar(df, x='contract_end_date', y='status', color='status', title="Saintes por mês")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        status_counts = df.groupby(['status', 'Quem Enviou Última Mensagem']).size().unstack()
        fig = px.bar(status_counts, barmode='group', title="Status do Usuário em relação a quem enviou a última mensagem")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_sairam = df[df['status'] == 'lost']

        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '>80']
        df_sairam['Faixa Etária'] = pd.cut(df_sairam['birthdate'], bins=bins, labels=labels, right=False)

        age_counts = df_sairam['Faixa Etária'].value_counts().reset_index()
        age_counts.columns = ['Faixa Etária', 'Quantidade']

        fig = px.pie(age_counts, names='Faixa Etária', values='Quantidade', title='Distribuição de Faixa Etária das Pessoas que Sairam', hole=0.4)

        st.plotly_chart(fig, use_container_width=True)

    # Gráfico de linha com a quantidade de entrantes e saíntes por mês
    df['contract_start_date'] = pd.to_datetime(df['contract_start_date'])
    df['contract_end_date'] = pd.to_datetime(df['contract_end_date'])

    # Contando entrantes e saintes por data
    entrantes = df['contract_start_date'].value_counts().sort_index()
    saintes = df['contract_end_date'].value_counts().sort_index()

    # Criando um DataFrame com entrantes e saintes
    timeline_df = pd.DataFrame({'Entrantes': entrantes, 'Saintes': saintes})

    # Reindexando o DataFrame para incluir todas as datas entre o mínimo e o máximo
    idx = pd.date_range(timeline_df.index.min(), timeline_df.index.max())
    timeline_df = timeline_df.reindex(idx, fill_value=0)

    # Calculando o total acumulado de entrantes e saintes
    timeline_df['Total Entrantes'] = timeline_df['Entrantes'].cumsum()
    timeline_df['Total Saintes'] = timeline_df['Saintes'].cumsum()

    # Resetando o índice para transformar as datas em uma coluna
    timeline_df = timeline_df.reset_index().rename(columns={'index': 'Data'})

    # Criando o gráfico de linha com Plotly Express
    fig = px.line(timeline_df, x='Data', y=['Total Entrantes', 'Total Saintes'], title='Número Total de Entrantes e Saintes ao Longo do Tempo')
    st.plotly_chart(fig, use_container_width=True)

    
