import sqlite3

# Função para criar a tabela do banco de dados se ela não existir
def criar_tabelas():
    conn = sqlite3.connect('afeto_sabor.db')
    cursor = conn.cursor()

    # Criar tabela para armazenar as entradas e saídas de estoque
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor REAL NOT NULL,
        nota_fiscal TEXT NOT NULL,
        horario TEXT NOT NULL
    )
    ''')

    # Criar tabela para armazenar os produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL
    )
    ''')

    # Criar tabela para armazenar o histórico de notas fiscais
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notas_fiscais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nota_fiscal TEXT NOT NULL,
        horario TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Chamar a função para garantir que as tabelas sejam criadas ao iniciar o aplicativo
criar_tabelas()