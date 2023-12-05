import streamlit as st
import bcrypt
from pymongo import MongoClient
from datetime import datetime

# Substitua as configurações do MongoDB com as suas próprias


def connect_to_mongodb():
    client = MongoClient(st.secrets.mongo.mongo_uri)
    db = client[st.secrets.mongo.mongo_db]
    return db

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
            db = connect_to_mongodb()

            # Inserir o usuário no banco de dados
            users = db.users
            users.insert_one({
                "username": username,
                "password": hashed.decode('utf-8'),
                "email": email
            })

            # Criar um log de autenticação
            auth_logs = db.auth_logs
            auth_logs.insert_one({
                "username": username,
                "time": datetime.now(),
                "type": "register"
            })

        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return False

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

if __name__ == "__main__":
    cadastro()
