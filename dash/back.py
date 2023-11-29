from flask import Flask, request
import sqlite3
import bcrypt

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def cadastro():
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    data = request.get_json()

    valid_keys = ['email', 'password']
    for key in valid_keys:
        if key not in data:
            return 'Missing key - {}'.format(key), 400
        
    username = data['email']
    password = data['password'].encode('utf-8')

    if "@anahealth.app" not in username:
        return {"mensagem": "Email inválido!"}, 400

    # Gerar um hash da senha
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # inserir com a senha hasheada
    cursor.execute("""
        INSERT INTO users (email, password)
        VALUES (?, ?)
    """, (username, hashed))

    conn.commit()
    conn.close()

    return {"mensagem": "Usuário cadastrado com sucesso!"}, 201

@app.route('/login', methods=['POST'])
def login():
    conn = sqlite3.connect('db/database.db')
    cursor = conn.cursor()

    data = request.get_json()

    valid_keys = ['email', 'password']
    for key in valid_keys:
        if key not in data:
            return 'Missing key - {}'.format(key), 400
        
    username = data['email']
    password = data['password'].encode('utf-8')

    # consultar
    cursor.execute("""
        SELECT * FROM users
        WHERE email=?
    """, (username,))

    user = cursor.fetchone()

    if user and bcrypt.checkpw(password, user[1]): 
        conn.commit()
        conn.close()
        return {"mensagem": "Usuário autenticado com sucesso!"}, 200
    else:
        conn.commit()
        conn.close()
        return {"mensagem": "E-mail ou senha inválidos!"}, 401


if __name__ == '__main__':
    app.run(debug=True)
