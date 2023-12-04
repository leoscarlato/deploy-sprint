import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
import streamlit_shadcn_ui as ui
from script_dataframe import tratamento

def dashboard():
    st.title("📈 Dashboard")

    df = st.session_state.get('df', None)

    if df is None:
        return
    
    df = st.session_state.df

    st.session_state['data_inicial'] = pd.to_datetime(st.session_state['data_inicial'])
    st.session_state['data_final'] = pd.to_datetime(st.session_state['data_final'])

    df_filtrado = df[(df['contract_start_date'] >= st.session_state['data_inicial']) &
                    (df['contract_start_date'] <= st.session_state['data_final'])]

    # ===================================== Número de pessoas com contrato ativo =================================================================

    # contrato ativo -> contract_end_date = NaT e status = won
    count_active_users = df_filtrado[(df_filtrado['contract_end_date'].isna()) & (df_filtrado['status'] == 'won')]['status'].count().astype(str)
    count_active_users = count_active_users + " pessoas"

    col1, col2 = st.columns(2)

    with col1:
        ui.metric_card("Número de pessoas que ativaram o contrato", count_active_users, "👥")

    # =============================================================================================================================================

    # ===================================== Número de pessoas com contrato cancelado ===========================================================

    # contrato cancelado -> contract_end_date != NaT e status = lost
    count_canceled_users = df_filtrado[(df_filtrado['contract_end_date'].notna()) & (df_filtrado['status'] == 'lost')]['status'].count().astype(str)
    count_canceled_users = count_canceled_users + " pessoas"

    with col2:
        ui.metric_card("Número de pessoas que cancelaram o contrato", count_canceled_users, "👥")

    # =============================================================================================================================================

    # ===================================== Gráfico de barras com a quantidade de entrantes e saintes por mês =====================================

    # Agrupar por mês e status, e contar as ocorrências
    df_grouped = df_filtrado.groupby([df_filtrado['contract_end_date'].dt.strftime('%Y-%m'), 'status']).size().reset_index(name='Contagem')

    # Criar o gráfico de barras
    fig = px.bar(df_grouped, x=df_grouped['contract_end_date'], y='Contagem', color='status', title="Saintes por mês")

    # Atualizar layout para ocultar a legenda
    fig.update_layout(showlegend=False)

    # Mostrar o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # =============================================================================================================================================

    col1, col2 = st.columns(2)

    with col1:

        # ===================================== Gráfico de quem enviou a última mensagem =====================================

        status_counts = df_filtrado.groupby(['status', 'Quem Enviou Última Mensagem']).size().unstack()
        fig = px.bar(status_counts, barmode='group', title="Status do Usuário em relação a quem enviou a última mensagem")
        st.plotly_chart(fig, use_container_width=True)

        # ====================================================================================================================

    with col2:

        # ===================================== Gráfico das faixas etárias dos clientes que saíram =====================================

        df_sairam = df_filtrado[df_filtrado['status'] == 'lost']

        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '>80']
        df_sairam['Faixa Etária'] = pd.cut(df_sairam['birthdate'], bins=bins, labels=labels, right=False)

        age_counts = df_sairam['Faixa Etária'].value_counts().reset_index()
        age_counts.columns = ['Faixa Etária', 'Quantidade']

        fig = px.pie(age_counts, names='Faixa Etária', values='Quantidade', title='Distribuição de Faixa Etária das Pessoas que Sairam', hole=0.4)

        st.plotly_chart(fig, use_container_width=True)

        # ================================================================================================================================

    # ====================================== Gráfico de linha com a quantidade de entrantes e saíntes por mês ============================

    df_filtrado['contract_start_date'] = pd.to_datetime(df_filtrado['contract_start_date'])
    df_filtrado['contract_end_date'] = pd.to_datetime(df_filtrado['contract_end_date'])

    entrantes = df_filtrado['contract_start_date'].value_counts().sort_index()
    saintes = df_filtrado['contract_end_date'].value_counts().sort_index()

    timeline_df = pd.DataFrame({'Entrantes': entrantes, 'Saintes': saintes})

    idx = pd.date_range(timeline_df.index.min(), timeline_df.index.max())
    timeline_df = timeline_df.reindex(idx, fill_value=0)

    timeline_df['Total Entrantes'] = timeline_df['Entrantes'].cumsum()
    timeline_df['Total Saintes'] = timeline_df['Saintes'].cumsum()

    timeline_df = timeline_df.reset_index().rename(columns={'index': 'Data'})

    fig = px.line(timeline_df, x='Data', y=['Total Entrantes', 'Total Saintes'], title='Número Total de Entrantes e Saintes ao Longo do Tempo')
    st.plotly_chart(fig, use_container_width=True)

    # ======================================================================================================================================

    # ====================================== Gráfico dos planos de saúde mais comuns =======================================================

    col1, col2 = st.columns(2)

    with col1:
    
        df_filtrado['id_health_plan'] = df_filtrado['id_health_plan'].fillna('Não Informado')
        df_filtrado['id_health_plan'] = df_filtrado['id_health_plan'].replace(412, 'SUS')
        df_filtrado['id_health_plan'] = df_filtrado['id_health_plan'].apply(lambda x: 'Particular' if isinstance(x, float) and not pd.isnull(x) else x)

        # Agora filtre para status 'won' após ter feito as substituições
        df_plan_mais_comum = df_filtrado[df_filtrado['status'] == 'won']

        # Contagem de valores de 'id_health_plan' para as linhas filtradas
        data = df_plan_mais_comum['id_health_plan'].value_counts().reset_index()
        data.columns = ['id_health_plan', 'count']

        # Crie o gráfico de pizza com os dados corrigidos
        fig = px.pie(data, names='id_health_plan', values='count', title='Planos de Saúde Mais Comuns', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # ======================================================================================================================================

    # ================================================ Tipos de Atendimento ===============================================================
    
    with col2:
    
        labels = ["Médico", "Acolhimento", "Psicoterapia"]
        values = [df_filtrado["Qde Atendimento Médico"].sum(), df_filtrado["Qde Atendimentos Acolhimento"].sum(), df_filtrado["Qde Psicoterapia"].sum()]

        fig = px.pie(values=values, names=labels, title="Quantidade de Cada Tipo de Atendimento", hole=0.4) 
        st.plotly_chart(fig, use_container_width=True)

    # ======================================================================================================================================

    # ================================================ Ranking top problemas abertos =======================================================

    