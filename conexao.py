import sqlite3

def criarConexao():
    try:
        conn = sqlite3.connect("ad2.db")
        return conn
    except NameError as erro:
        print("Erro ao criar ou conectar com o banco:", erro)

def fecharConexao(conexao):
    conexao.close()