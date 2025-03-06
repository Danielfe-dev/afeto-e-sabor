import tkinter as tk
from tkinter import ttk
from estoque import adicionar_entrada, registrar_saida, buscar_historico

# Criar a janela principal
janela = tk.Tk()
janela.title("Afeto e Sabor - Controle de Estoque")
janela.geometry("600x400")

# Criar o notebook (abas)
abas = ttk.Notebook(janela)
abas.pack(expand=True, fill="both")

# Criar abas
aba_controle = ttk.Frame(abas)
aba_estoque = ttk.Frame(abas)
aba_notas = ttk.Frame(abas)

abas.add(aba_controle, text="Controle de Estoque")
abas.add(aba_estoque, text="Visualizar Estoque")
abas.add(aba_notas, text="Notas Fiscais")

# -----------------------------------------
# 🔹 Aba 1: Controle de Estoque
# -----------------------------------------

tk.Label(aba_controle, text="Nome da Camisa:").pack()
entrada_nome = tk.Entry(aba_controle)
entrada_nome.pack()

tk.Label(aba_controle, text="Quantidade:").pack()
entrada_quantidade = tk.Entry(aba_controle)
entrada_quantidade.pack()

def atualizar_listas():
    atualizar_estoque()
    atualizar_notas()

def adicionar():
    nome = entrada_nome.get()
    quantidade = entrada_quantidade.get()
    
    if nome and quantidade.isdigit():
        adicionar_entrada(nome, int(quantidade))
        atualizar_listas()

def retirar():
    nome = entrada_nome.get()
    quantidade = entrada_quantidade.get()
    
    if nome and quantidade.isdigit():
        registrar_saida(nome, int(quantidade))
        atualizar_listas()

botao_adicionar = tk.Button(aba_controle, text="Adicionar Entrada", command=adicionar)
botao_adicionar.pack()

botao_retirar = tk.Button(aba_controle, text="Registrar Saída", command=retirar)
botao_retirar.pack()

# -----------------------------------------
# 🔹 Aba 2: Visualizar Estoque
# -----------------------------------------

lista_estoque = tk.Listbox(aba_estoque, width=80, height=10)
lista_estoque.pack()

def atualizar_estoque():
    lista_estoque.delete(0, tk.END)
    estoque_atual = {}  # Dicionário para contar as quantidades
    transacoes = buscar_historico()  # Buscar transações do banco de dados

    for transacao in transacoes:
        tipo, nome, quantidade = transacao[1], transacao[2], transacao[3]
        if tipo == "Entrada":
            estoque_atual[nome] = estoque_atual.get(nome, 0) + quantidade
        elif tipo == "Saída":
            estoque_atual[nome] = estoque_atual.get(nome, 0) - quantidade

    for nome, quantidade in estoque_atual.items():
        lista_estoque.insert(tk.END, f"{nome}: {quantidade} unidades")

# -----------------------------------------
# 🔹 Aba 3: Notas Fiscais
# -----------------------------------------

lista_notas = tk.Listbox(aba_notas, width=80, height=10)
lista_notas.pack()

def atualizar_notas():
    lista_notas.delete(0, tk.END)
    transacoes = buscar_historico()  # Buscar transações do banco de dados

    for transacao in transacoes:
        tipo, nota_fiscal, horario = transacao[1], transacao[4], transacao[5]
        lista_notas.insert(tk.END, f"{tipo} - {nota_fiscal} - {horario}")

# Atualizar listas na inicialização
atualizar_listas()

# Iniciar a interface
janela.mainloop()
