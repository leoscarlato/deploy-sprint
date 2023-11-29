import streamlit as st
from paginas.cadastro import cadastro
from paginas.login import login
from paginas.dados import dados
from streamlit_option_menu import option_menu
from paginas.dashboard import dashboard

# Inicializando o estado de login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def main():
    st.set_page_config(page_title="Dash", page_icon="📊", layout="wide")

    # Mostrar as opções de login e cadastro fora da barra lateral
    if not st.session_state['logged_in']:
        tab_login, tab_cadastro = st.tabs(["Login", "Cadastro"])

        with tab_login:
            if login():
                st.session_state['logged_in'] = True
                st.experimental_rerun()  # Reinicia o aplicativo para atualizar a navegação

        with tab_cadastro:
            cadastro()

    # Configurar a barra lateral para navegação após o login
    if st.session_state['logged_in']:
        with st.sidebar:
            st.title("Menu")
            page = option_menu("Navegar",
                               options=["Dados", "Dashboard"],
                               icons=["📊", "📈"],
                               menu_icon="cast", default_index=0)

        if page == "Dados":
            dados()
        elif page == "Dashboard":
            dashboard()

        # logout
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['df'] = None
            st.experimental_rerun()  # Reinicia o aplicativo para atualizar a navegação

if __name__ == "__main__":
    main()
