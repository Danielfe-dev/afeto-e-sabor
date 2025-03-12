import uuid
import sqlite3
from datetime import datetime

# Conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect('afeto_sabor.db')

# Função para adicionar entrada no estoque
def adicionar_entrada(nome, quantidade, valor, codigo):
    nota_fiscal = str(uuid.uuid4())[:8]  # Gerar número único da nota fiscal
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Registrar horário
    
    conn = conectar_bd()
    cursor = conn.cursor()

    # Inserir produto na tabela produtos
    cursor.execute('''
    INSERT OR IGNORE INTO produtos (nome, valor)
    VALUES (?, ?)
    ''', (nome, valor))

    # Inserir transação na tabela transacoes
    cursor.execute('''
    INSERT INTO transacoes (tipo, nome, quantidade, valor, nota_fiscal, horario)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Entrada', nome, quantidade, valor, nota_fiscal, horario))

    conn.commit()
    conn.close()

    return nota_fiscal, horario

# Função para verificar estoque disponível
def verificar_estoque(nome):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT SUM(CASE WHEN tipo = 'Entrada' THEN quantidade ELSE -quantidade END)
    FROM transacoes WHERE nome = ?
    ''', (nome,))

    resultado = cursor.fetchone()[0]
    conn.close()

    return resultado if resultado else 0  # Retorna 0 se não houver registros

# Função para registrar saída do estoque
def registrar_saida(nome, quantidade):
    estoque_disponivel = verificar_estoque(nome)

    if estoque_disponivel < quantidade:
        return None, f"Erro: Apenas {estoque_disponivel} unidades disponíveis."

    nota_fiscal = str(uuid.uuid4())[:8]
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar_bd()
    cursor = conn.cursor()

    valor = buscar_valor_produto(nome)
    if valor is None:
        return None, "Erro: Produto não encontrado no banco de dados."

    cursor.execute('''
    INSERT INTO transacoes (tipo, nome, quantidade, valor, nota_fiscal, horario)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Saída', nome, quantidade, valor, nota_fiscal, horario))

    conn.commit()
    conn.close()

    return nota_fiscal, horario

# Função para buscar transações no banco
def buscar_historico():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transacoes')
    transacoes = cursor.fetchall()

    conn.close()
    
    return transacoes

# Função para buscar valor do produto no banco
def buscar_valor_produto(nome):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT valor FROM produtos WHERE nome = ?', (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Função para remover produto do registro do estoque
def remover_produto(nome):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM transacoes WHERE nome = ?
    ''', (nome,))

    conn.commit()
    conn.close()

    print(f"Produto '{nome}' removido do registro do estoque.")

# Função para alterar informações do produto
def alterar_produto(nome_antigo, nome_novo, valor_novo):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE produtos
    SET nome = ?, valor = ?
    WHERE nome = ?
    ''', (nome_novo, valor_novo, nome_antigo))

    conn.commit()
    conn.close()

    print(f"Produto '{nome_antigo}' atualizado para '{nome_novo}' com valor R${valor_novo:.2f}.")