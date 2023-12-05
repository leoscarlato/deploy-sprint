import streamlit as st
import bcrypt
import mysql.connector
from mysql.connector import Error


def cadastrar_usuario(email, username, password):
    # Gerar um hash da senha
    password_encoded = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_encoded, bcrypt.gensalt())

    if email == "" or password == "" or username == "":
        st.error("Erro ao cadastrar usuário!")
        return False
    else:
        if "@anahealth.app" not in email:
            st.error("E-mail inválido!")
            return False

        try:

            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(st.secrets.connections.username)
            conn = mysql.connector.connect(
                user = st.secrets.connections.username,
                password = st.secrets.connections.password,
                host = st.secrets.connections.host,
                database = st.secrets.connections.database
            )
            
            cursor = conn.cursor()

            # Inserir o usuário no banco de dados
            query = """
                INSERT INTO users (username, password, email)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (username, hashed.decode('utf-8'), email))

            # Criar um log de autenticação
            query = """
                INSERT INTO auth_logs (username, time, type)
                VALUES (%s, NOW(), 'register')
            """
            cursor.execute(query, (username,))

            # Salvar as alterações
            conn.commit()

        except Error as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
        st.success("Cadastro realizado com sucesso!")
        return True

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.button("Cadastro")

    if submit:
        cadastrar_usuario(email, username, password)
