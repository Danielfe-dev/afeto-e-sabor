import os
from tkinter import filedialog

# Função para salvar nota fiscal
def salvar_nota_fiscal(nota_fiscal, nome, quantidade, horario):
    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivo de Texto", "*.txt"), ("PDF", "*.pdf")],
        title="Salvar Nota Fiscal"
    )
    
    if not caminho:
        return

    conteudo = f"Nota Fiscal: {nota_fiscal}\nProduto: {nome}\nQuantidade: {quantidade}\nData e Hora: {horario}\n"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    print(f"Nota fiscal salva em {caminho}")