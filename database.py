import sqlite3

# Conecte-se ao banco de dados (ou crie um se não existir)
conn = sqlite3.connect('banco.db')
conn.execute("PRAGMA foreign_keys = 1")  # Ative a verificação de chaves estrangeiras

# Crie um cursor
cursor = conn.cursor()

# Crie a tabela clientes com um campo para senha
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")

# Crie a tabela contas
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    numero INTEGER PRIMARY KEY AUTOINCREMENT,
    agencia TEXT NOT NULL,
    cliente_id INTEGER NOT NULL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")

# Crie a tabela transacoes
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    conta_numero INTEGER NOT NULL,
    data_hora TEXT NOT NULL,
    FOREIGN KEY(conta_numero) REFERENCES contas(numero)
)
""")
