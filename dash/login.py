import streamlit as st
import bcrypt
from pymongo import MongoClient
from datetime import datetime

# Substitua as configurações do MongoDB com as suas próprias

def connect_to_mongodb():
    client = MongoClient(st.secrets.mongo.mongo_uri)
    db = client[st.secrets.mongo.mongo_db]
    return db

def buscar_username(email):
    try:
        db = connect_to_mongodb()

        user = db.users.find_one({"email": email}, {"username": 1})
        return user["username"] if user else None

    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def verifica_usuario(email, senha):
    try:
        db = connect_to_mongodb()

        user = db.users.find_one({"email": email}, {"password": 1})
        if user:
            stored_password_hash = user["password"]
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')

            if bcrypt.checkpw(senha.encode('utf-8'), stored_password_hash):
                return True
            else:
                return False
        else:
            return False

    except Exception as e:
        st.error(f"Erro durante a autenticação: {e}")
        return False

def login():
    st.title("Login")

    with st.form(key="login_form"):
        email = st.text_input("Email", key="email_login")
        password = st.text_input("Password", type="password", key="password_login")
        submit = st.form_submit_button("Fazer Login")

    if submit:
        if verifica_usuario(email, password):
            username = buscar_username(email)

            try:
                db = connect_to_mongodb()
                auth_logs = db.auth_logs

                auth_logs.insert_one({
                    "username": username,
                    "time": datetime.now(),
                    "type": "login"
                })

            except Exception as e:
                st.error(f"Erro ao conectar ao banco de dados: {e}")

            st.session_state['user_name'] = username
            st.success("Login realizado com sucesso!")
            return True
        else:
            st.error("Erro ao realizar login!")

            try:
                db = connect_to_mongodb()
                auth_logs = db.auth_logs

                auth_logs.insert_one({
                    "username": email,
                    "time": datetime.now(),
                    "type": "failed_login"
                })

            except Exception as e:
                st.error(f"Erro ao conectar ao banco de dados: {e}")

            return False

if __name__ == "__main__":
    login()
