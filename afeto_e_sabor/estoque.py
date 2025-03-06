import uuid
import sqlite3
from datetime import datetime

# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect('afeto_sabor.db')

# Função para adicionar uma entrada no estoque
def adicionar_entrada(nome, quantidade):
    nota_fiscal = str(uuid.uuid4())[:8]  # Gera um número único de 8 caracteres
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Captura data e hora
    
    # Conectar ao banco de dados e registrar a entrada
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO transacoes (tipo, nome, quantidade, nota_fiscal, horario)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Entrada', nome, quantidade, nota_fiscal, horario))
    
    conn.commit()
    conn.close()
    
    return nota_fiscal, horario  # Retorna os valores para exibição na interface

# Função para registrar uma saída no estoque
def registrar_saida(nome, quantidade):
    nota_fiscal = str(uuid.uuid4())[:8]
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Conectar ao banco de dados e registrar a saída
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transacoes (tipo, nome, quantidade, nota_fiscal, horario)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Saída', nome, quantidade, nota_fiscal, horario))

    conn.commit()
    conn.close()

    return nota_fiscal, horario  # Retorna os valores para exibição na interface

# Função para buscar o histórico de transações (entradas e saídas)
def buscar_historico():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transacoes')
    transacoes = cursor.fetchall()

    conn.close()
    
    return transacoes
