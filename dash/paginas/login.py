import streamlit as st
import bcrypt
import mysql.connector
from mysql.connector import Error

# Configurações do banco de dados MySQL
db_config = {
    'database': st.secrets["connections.mysql"]['database'],
    'user': st.secrets["connections.mysql"]['user'],
    'password': st.secrets["connections.mysql"]['password'],
    'host': st.secrets["connections.mysql"]['host']
}

def buscar_username(email):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT username FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        username = cursor.fetchone()

        return username[0] if username else None

    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def verifica_usuario(email, senha):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            stored_password_hash = user[0]
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')
            
            if bcrypt.checkpw(senha.encode('utf-8'), stored_password_hash):
                return True
            else:
                return False
        else:
            return False
        
    except Error as e:
        st.error(f"Erro durante a autenticação: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def login():
    st.title("Login")
    
    email = st.text_input("Email", key="email_login")
    password = st.text_input("Password", type="password", key="password_login")
    submit = st.button("Login")

    if submit:
        if verifica_usuario(email, password): 
            username = buscar_username(email)

            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                query = """
                    INSERT INTO auth_logs (username, time, type)
                    VALUES (%s, NOW(), 'login')
                """
                cursor.execute(query, (username,))
                conn.commit()

            except Error as e:
                st.error(f"Erro ao conectar ao banco de dados: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

            st.session_state['user_name'] = username           
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Erro ao realizar login!")

            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                query = """
                    INSERT INTO auth_logs (username, time, type)
                    VALUES (%s, NOW(), 'failed_login')
                """
                cursor.execute(query, (email,))
                conn.commit()

            except Error as e:
                st.error(f"Erro ao conectar ao banco de dados: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
            
            return False
