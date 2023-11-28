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

    
