import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style, WARNING
from estoque import adicionar_entrada, registrar_saida, buscar_historico, verificar_estoque, remover_produto, buscar_valor_produto, alterar_produto
from notas_fiscais import gerar_nota_fiscal_txt, gerar_nota_fiscal_pdf  # Importar as funções de geração de notas fiscais
import uuid
import sqlite3  # Importar a biblioteca sqlite3 para conexão com o banco de dados

def conectar_bd():
    return sqlite3.connect('afeto_sabor.db')

def buscar_produto_por_codigo(codigo_barras):
    # Esta função deve buscar o produto pelo código de barras no banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, quantidade, valor FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
    produto = cursor.fetchone()
    conn.close()
    if produto:
        return {'nome': produto[0], 'quantidade': produto[1], 'valor': produto[2]}
    else:
        return None

def iniciar_janela():
    janela = tk.Tk()
    janela.title("Afeto e Sabor - Controle de Estoque")
    janela.geometry("1024x768")  # Ajuste o tamanho da janela para computadores
    janela.configure(bg='#FFD700')  # Dark yellow background

    # Aplicar estilo ttkbootstrap com tema personalizado
    style = Style(theme="flatly")
    
    # Configurar estilo dos botões e widgets
    style.configure("TButton", foreground="white", background="orange", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12), foreground="black")
    style.configure("TLabel", font=("Helvetica", 12), background='#FFD700', foreground="black", anchor="w")
    style.configure("TFrame", background='#FFD700')
    style.configure("TNotebook", background='#FFD700')
    style.configure("TNotebook.Tab", background='#FFD700')

    # Criar abas
    abas = ttk.Notebook(janela)
    abas.pack(expand=True, fill="both", padx=10, pady=10)

    aba_entrada = ttk.Frame(abas)
    aba_saida = ttk.Frame(abas)
    aba_estoque = ttk.Frame(abas)
    aba_notas = ttk.Frame(abas)
    aba_alterar = ttk.Frame(abas)

    # Container principal para cada aba
    container_entrada = ttk.Frame(aba_entrada)
    container_entrada.pack(side="left", padx=20, pady=20, anchor="nw")

    container_saida = ttk.Frame(aba_saida)
    container_saida.pack(side="left", padx=20, pady=20, anchor="nw")
    
    container_estoque = ttk.Frame(aba_estoque)
    container_estoque.pack(side="left", padx=20, pady=20, anchor="nw")
    
    container_notas = ttk.Frame(aba_notas)
    container_notas.pack(side="left", padx=20, pady=20, anchor="nw")

    container_alterar = ttk.Frame(aba_alterar)
    container_alterar.pack(side="left", padx=20, pady=20, anchor="nw")

    abas.add(aba_entrada, text="Entrada de Produtos")
    abas.add(aba_saida, text="Saída de Produtos")
    abas.add(aba_estoque, text="Visualizar Estoque")
    abas.add(aba_notas, text="Notas Fiscais")
    abas.add(aba_alterar, text="Alterar Produto")

    # -----------------------------------------
    # 🔹 Aba 1: Entrada de Produtos
    # -----------------------------------------

    ttk.Label(container_entrada, text="Nome da Camisa:").pack(pady=5, anchor="w")
    entrada_nome = ttk.Entry(container_entrada)
    entrada_nome.pack(pady=5, anchor="w")

    ttk.Label(container_entrada, text="Quantidade:").pack(pady=5, anchor="w")
    entrada_quantidade = ttk.Entry(container_entrada)
    entrada_quantidade.pack(pady=5, anchor="w")

    ttk.Label(container_entrada, text="Valor:").pack(pady=5, anchor="w")
    entrada_valor = ttk.Entry(container_entrada)
    entrada_valor.pack(pady=5, anchor="w")

    ttk.Label(container_entrada, text="Código de Barras:").pack(pady=5, anchor="w")
    entrada_codigo_barras = ttk.Entry(container_entrada)
    entrada_codigo_barras.pack(pady=5, anchor="w")

    botao_ler_codigo_barras_entrada = ttk.Button(container_entrada, text="Ler Código de Barras", style="warning.TButton")
    botao_ler_codigo_barras_entrada.pack(pady=10, anchor="w")

    def atualizar_listas():
        atualizar_estoque()
        atualizar_notas()

    def adicionar():
        nome = entrada_nome.get()
        quantidade = entrada_quantidade.get()
        valor = entrada_valor.get()
        
        if nome and quantidade.isdigit() and valor.replace('.', '', 1).isdigit():
            nota_fiscal, horario = adicionar_entrada(nome, int(quantidade), float(valor), "")
            atualizar_listas()
            messagebox.showinfo("Entrada Adicionada", f"Nota Fiscal: {nota_fiscal}\nHorário: {horario}")

    botao_adicionar = ttk.Button(container_entrada, text="Adicionar Entrada", command=adicionar, style="warning.TButton")
    botao_adicionar.pack(pady=10, anchor="w")

    # Função para capturar entrada de código de barras
    def capturar_codigo_barras_entrada(event):
        codigo_barras = entrada_codigo_barras.get()
        produto = buscar_produto_por_codigo(codigo_barras)
        if produto:
            entrada_nome.delete(0, tk.END)
            entrada_nome.insert(0, produto['nome'])
            entrada_quantidade.delete(0, tk.END)
            entrada_quantidade.insert(0, produto['quantidade'])
            entrada_valor.delete(0, tk.END)
            entrada_valor.insert(0, produto['valor'])
        else:
            messagebox.showerror("Erro", "Produto não encontrado para o código de barras fornecido.")
        print(f"Código de barras capturado (entrada): {codigo_barras}")

    entrada_codigo_barras.bind("<Return>", capturar_codigo_barras_entrada)

    # -----------------------------------------
    # 🔹 Aba 2: Saída de Produtos
    # -----------------------------------------

    ttk.Label(container_saida, text="Nome da Camisa:").pack(pady=5, anchor="w")
    saida_nome = ttk.Entry(container_saida)
    saida_nome.pack(pady=5, anchor="w")

    ttk.Label(container_saida, text="Quantidade:").pack(pady=5, anchor="w")
    saida_quantidade = ttk.Entry(container_saida)
    saida_quantidade.pack(pady=5, anchor="w")

    ttk.Label(container_saida, text="Código de Barras:").pack(pady=5, anchor="w")
    saida_codigo_barras = ttk.Entry(container_saida)
    saida_codigo_barras.pack(pady=5, anchor="w")

    botao_ler_codigo_barras_saida = ttk.Button(container_saida, text="Ler Código de Barras", style="warning.TButton")
    botao_ler_codigo_barras_saida.pack(pady=10, anchor="w")

    lista_itens = tk.Listbox(container_saida, width=80, height=10, font=("Helvetica", 12))
    lista_itens.pack(pady=5, anchor="w")

    total_label = ttk.Label(container_saida, text="Total: R$0.00", font=("Helvetica", 12), background='#FFD700', anchor="w")
    total_label.pack(pady=5, anchor="w")

    itens = []
    total = 0.0

    def adicionar_item():
        nome = saida_nome.get()
        quantidade = saida_quantidade.get()
        
        if nome and quantidade.isdigit():
            quantidade = int(quantidade)
            valor = buscar_valor_produto(nome)
            if valor is not None:
                total_item = quantidade * valor
                itens.append((nome, quantidade, valor, total_item))
                lista_itens.insert(tk.END, f"{nome} - {quantidade} x R${valor:.2f} = R${total_item:.2f}")
                atualizar_total()
            else:
                messagebox.showerror("Erro", "Produto não encontrado no banco de dados.")
        else:
            messagebox.showerror("Erro", "Nome do produto ou quantidade inválidos.")

    def atualizar_total():
        nonlocal total
        total = sum(item[3] for item in itens)
        total_label.config(text=f"Total: R${total:.2f}")

    def finalizar_compra():
        if not itens:
            messagebox.showwarning("Aviso", "Nenhum item adicionado.")
            return

        for item in itens:
            nome, quantidade, valor, total_item = item
            nota_fiscal, horario = registrar_saida(nome, quantidade)
            if nota_fiscal is None:
                messagebox.showerror("Erro", horario)
                return

        nota_fiscal = str(uuid.uuid4())[:8]  # Gerar número único da nota fiscal
        local_compra = "Loja XYZ"
        gerar_nota_fiscal_txt("Compra", len(itens), total, local_compra, nota_fiscal)
        gerar_nota_fiscal_pdf("Compra", len(itens), total, local_compra, nota_fiscal)
        messagebox.showinfo("Compra Finalizada", f"Nota Fiscal: {nota_fiscal}\nTotal: R${total:.2f}")
        itens.clear()
        lista_itens.delete(0, tk.END)
        atualizar_total()

    botao_adicionar_item = ttk.Button(container_saida, text="Adicionar Item", command=adicionar_item, style="warning.TButton")
    botao_adicionar_item.pack(pady=10, anchor="w")

    botao_finalizar_compra = ttk.Button(container_saida, text="Finalizar Compra", command=finalizar_compra, style="warning.TButton")
    botao_finalizar_compra.pack(pady=10, anchor="w")

    # Função para capturar entrada de código de barras
    def capturar_codigo_barras_saida(event):
        codigo_barras = saida_codigo_barras.get()
        produto = buscar_produto_por_codigo(codigo_barras)
        if produto:
            saida_nome.delete(0, tk.END)
            saida_nome.insert(0, produto['nome'])
            saida_quantidade.delete(0, tk.END)
            saida_quantidade.insert(0, produto['quantidade'])
        else:
            messagebox.showerror("Erro", "Produto não encontrado para o código de barras fornecido.")
        print(f"Código de barras capturado (saída): {codigo_barras}")

    saida_codigo_barras.bind("<Return>", capturar_codigo_barras_saida)

    # -----------------------------------------
    # 🔹 Aba 3: Visualizar Estoque
    # -----------------------------------------

    lista_estoque = tk.Listbox(container_estoque, width=80, height=10, font=("Helvetica", 12))
    lista_estoque.pack(pady=5, anchor="w")

    def atualizar_estoque():
        lista_estoque.delete(0, tk.END)
        estoque_atual = {}  
        transacoes = buscar_historico()

        for transacao in transacoes:
            tipo, nome, quantidade = transacao[1], transacao[2], transacao[3]
            if tipo == "Entrada":
                estoque_atual[nome] = estoque_atual.get(nome, 0) + quantidade
            elif tipo == "Saída":
                estoque_atual[nome] = estoque_atual.get(nome, 0) - quantidade

        for nome, quantidade in estoque_atual.items():
            lista_estoque.insert(tk.END, f"{nome}: {quantidade} unidades")

    ttk.Label(container_estoque, text="Nome do Produto para Remover:").pack(pady=5, anchor="w")
    entrada_nome_remover = ttk.Entry(container_estoque)
    entrada_nome_remover.pack(pady=5, anchor="w")

    def remover():
        nome = entrada_nome_remover.get()
        if nome:
            remover_produto(nome)
            atualizar_listas()
            messagebox.showinfo("Produto Removido", f"O produto '{nome}' foi removido do registro de estoque.")
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome do produto para remover.")

    botao_remover = ttk.Button(container_estoque, text="Remover Produto", command=remover, style="warning.TButton")
    botao_remover.pack(pady=10, anchor="w")

    # -----------------------------------------
    # 🔹 Aba 4: Notas Fiscais
    # -----------------------------------------

    lista_notas = tk.Listbox(container_notas, width=80, height=10, font=("Helvetica", 12))
    lista_notas.pack(pady=5, anchor="w")

    def atualizar_notas():
        lista_notas.delete(0, tk.END)
        transacoes = buscar_historico()

        for transacao in transacoes:
            tipo, nota_fiscal, horario = transacao[1], transacao[4], transacao[5]
            lista_notas.insert(tk.END, f"{tipo} - {nota_fiscal} - {horario}")

    def imprimir_nota_selecionada():
        selecionado = lista_notas.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para imprimir.")
            return

        indice = selecionado[0]
        nota_fiscal_info = lista_notas.get(indice)
        
        partes = nota_fiscal_info.split(" - ")
        if len(partes) < 3:
            messagebox.showerror("Erro", "Formato inválido da nota fiscal.")
            return

        tipo, nota_fiscal, horario = partes
        gerar_nota_fiscal_txt("Produto Desconhecido", 1, 0.0, "Local Desconhecido", nota_fiscal)
        gerar_nota_fiscal_pdf("Produto Desconhecido", 1, 0.0, "Local Desconhecido", nota_fiscal)

    botao_imprimir_nota = ttk.Button(container_notas, text="Imprimir Nota Fiscal", 
                                   command=imprimir_nota_selecionada, style="warning.TButton")
    botao_imprimir_nota.pack(pady=10, anchor="w")

    # Atualizar listas ao iniciar
    atualizar_listas()

    # -----------------------------------------
    # 🔹 Aba 5: Alterar Produto
    # -----------------------------------------

    ttk.Label(container_alterar, text="Nome Atual do Produto:").pack(pady=5, anchor="w")
    alterar_nome_atual = ttk.Entry(container_alterar)
    alterar_nome_atual.pack(pady=5, anchor="w")

    ttk.Label(container_alterar, text="Novo Nome do Produto:").pack(pady=5, anchor="w")
    alterar_nome_novo = ttk.Entry(container_alterar)
    alterar_nome_novo.pack(pady=5, anchor="w")

    ttk.Label(container_alterar, text="Novo Valor do Produto:").pack(pady=5, anchor="w")
    alterar_valor_novo = ttk.Entry(container_alterar)
    alterar_valor_novo.pack(pady=5, anchor="w")

    def alterar():
        nome_atual = alterar_nome_atual.get()
        nome_novo = alterar_nome_novo.get()
        valor_novo = alterar_valor_novo.get()
        
        if nome_atual and nome_novo and valor_novo.replace('.', '', 1).isdigit():
            alterar_produto(nome_atual, nome_novo, float(valor_novo))
            atualizar_listas()
            messagebox.showinfo("Produto Alterado", f"Produto '{nome_atual}' atualizado para '{nome_novo}' com valor R${float(valor_novo):.2f}.")
        else:
            messagebox.showerror("Erro", "Informações inválidas para alteração.")

    botao_alterar = ttk.Button(container_alterar, text="Alterar Produto", command=alterar, style="warning.TButton")
    botao_alterar.pack(pady=10, anchor="w")

    # Iniciar o loop principal da janela
    janela.mainloop()

if __name__ == "__main__":
    iniciar_janela()