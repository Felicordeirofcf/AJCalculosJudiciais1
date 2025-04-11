import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "clientes.db")

def criar_banco():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            celular TEXT,
            email TEXT,
            oab TEXT
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_cliente(nome, celular, email, oab):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, celular, email, oab)
        VALUES (?, ?, ?, ?)
    """, (nome, celular, email, oab))
    conexao.commit()
    conexao.close()

def buscar_clientes():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def excluir_cliente(id_):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_,))
    conexao.commit()
    conexao.close()