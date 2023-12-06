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

    df = df.rename(columns={'birthdate': 'idade'})

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

    # ===================================== Gráfico de barras com a quantidade de saintes por mês =====================================

    df_grouped = df_filtrado.groupby([df_filtrado['contract_end_date'].dt.strftime('%Y-%m'), 'status']).size().reset_index(name='Contagem')
    df_grouped = df_grouped[(df_grouped['contract_end_date'] >= st.session_state['data_inicial'].strftime('%Y-%m')) &
                            (df_grouped['contract_end_date'] <= st.session_state['data_final'].strftime('%Y-%m'))]

    df_grouped['contract_end_date'] = pd.to_datetime(df_grouped['contract_end_date'], format='%Y-%m')

    df_grouped = df_grouped.sort_values(by='contract_end_date')

    fig = px.bar(df_grouped, x='contract_end_date', y='Contagem', color='status', barmode='group', title='Saintes por Mês')

    df_grouped['Média Móvel'] = df_grouped['Contagem'].rolling(3, min_periods=1).mean().round(2)

    fig.add_scatter(x=df_grouped['contract_end_date'], y=df_grouped['Média Móvel'], name='Média Móvel', mode='lines+markers', line=dict(color='red', width=2))
    fig.update_layout(xaxis_title='Data', yaxis_title='Contagem', legend_title='Legenda')
    fig.for_each_trace(lambda t: t.update(name="N° de saintes" if t.name == "lost" else t.name))

    st.plotly_chart(fig, use_container_width=True)

    # =============================================================================================================================================

    # ===================================== Gráfico de barras com a quantidade de entrantes por mês =====================================

    df_entrantes = df_filtrado[df_filtrado['status'] == 'won']

    # Agrupa por mês e status
    df_grouped = df_entrantes.groupby([df_entrantes['contract_start_date'].dt.strftime('%Y-%m'), 'status']).size().reset_index(name='Contagem')
    df_grouped = df_grouped[(df_grouped['contract_start_date'] >= st.session_state['data_inicial'].strftime('%Y-%m')) &
                            (df_grouped['contract_start_date'] <= st.session_state['data_final'].strftime('%Y-%m'))]

    df_grouped['contract_start_date'] = pd.to_datetime(df_grouped['contract_start_date'], format='%Y-%m')

    df_grouped = df_grouped.sort_values(by='contract_start_date')

    # Crie o gráfico de barras para os entrantes
    fig = px.bar(df_grouped, x='contract_start_date', y='Contagem', color='status', title='Entrantes por Mês')

    # Adicione a média móvel para os entrantes
    df_grouped['Média Móvel'] = df_grouped['Contagem'].rolling(3, min_periods=1).mean().round(2)
    fig.add_scatter(x=df_grouped['contract_start_date'], y=df_grouped['Média Móvel'], name='Média Móvel', mode='lines+markers', line=dict(color='red', width=2))

    fig.update_layout(xaxis_title='Data', yaxis_title='Contagem', legend_title='Legenda')
    fig.for_each_trace(lambda t: t.update(name="N° de entrantes" if t.name == "won" else t.name))

    # Use st.plotly_chart para exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


    # =============================================================================================================================================

    col1, col2, col3 = st.columns(3)
    with col1:
        # Mapeamento dos códigos de gênero para nomes
        gender_mapping = {63: 'Masculino', 64: 'Feminino', 117: 'Outros'}

        # Aplicando o mapeamento
        df_filtrado['gender_name'] = df_filtrado['id_gender'].map(gender_mapping)

        # Contando a quantidade de clientes por gênero mapeado
        gender_counts = df_filtrado['gender_name'].value_counts()

        # Criando o gráfico de pizza
        fig = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title='Distribuição de Clientes por Gênero', hole=0.4)

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)



        # ====================================================================================================================

    # ====================================== Gráfico dos planos de saúde mais comuns =======================================================


    with col2:
    
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
    
    with col3:
    
        labels = ["Médico", "Acolhimento", "Psicoterapia"]
        values = [df_filtrado["Qde Atendimento Médico"].sum(), df_filtrado["Qde Atendimentos Acolhimento"].sum(), df_filtrado["Qde Psicoterapia"].sum()]

        fig = px.pie(values=values, names=labels, title="Quantidade de Cada Tipo de Atendimento", hole=0.4) 
        st.plotly_chart(fig, use_container_width=True)

    # ======================================================================================================================================

    # ===================================== Gráfico das faixas etárias de todos os =====================================

    col1, col2 = st.columns(2)

    with col1:

        # Filtrando os clientes que estão ativos
        df_ativos = df_filtrado[df_filtrado['status'] == 'won']

        # Criando o gráfico de barras
        fig = px.histogram(df_ativos, x='idade', title='Faixa Etária dos Clientes Ativos', nbins=100)

        fig.update_layout(xaxis_title='Idade', yaxis_title='Contagem', legend_title='Legenda')

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # Filtrando os clientes que estão cancelados
        df_cancelados = df_filtrado[df_filtrado['status'] == 'lost']

        # Criando o gráfico de barras
        fig = px.histogram(df_cancelados, x='idade', title='Faixa Etária dos Clientes Que Cancelaram', nbins=100)

        fig.update_layout(xaxis_title='Idade', yaxis_title='Contagem', legend_title='Legenda')

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # ===============================================================================================================================