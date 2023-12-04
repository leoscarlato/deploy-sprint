import mysql.connector

# Conectar ao banco de dados MySQL
# Substitua 'mydb', 'user', 'password', 'host' com os detalhes do seu banco de dados MySQL
conn = mysql.connector.connect(
    database='anahealth',
    user='mcjac9esy23mrisdjorq',
    password='pscale_pw_USUCnX1syI5bgAXeObJducPgAEIVUWimt2Y7vTXNPXM',
    host='aws.connect.psdb.cloud'
)
cursor = conn.cursor()

# Criando a tabela de usuários
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
""")

# Criando a tabela de logs de autenticação
cursor.execute("""
    CREATE TABLE IF NOT EXISTS auth_logs (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        time DATETIME NOT NULL,
        type ENUM('login', 'logout', 'register') NOT NULL
    )
""")

conn.commit()
