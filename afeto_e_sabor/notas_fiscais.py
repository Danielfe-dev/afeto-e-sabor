from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import filedialog
import uuid

def gerar_nota_fiscal_txt(nome, quantidade, valor, local, nota_fiscal=None):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if nota_fiscal is None:
        nota_fiscal = str(uuid.uuid4())[3:11]  # Gerar número único da nota fiscal sem os três primeiros caracteres
    default_filename = f"NotaFiscal_{nota_fiscal}.txt"
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename, filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as arquivo:
            arquivo.write(f"Nota Fiscal: {nota_fiscal}\n")
            arquivo.write(f"Produto: {nome}\n")
            arquivo.write(f"Quantidade: {quantidade}\n")
            arquivo.write(f"Valor Unitário: R${valor:.2f}\n")
            arquivo.write(f"Valor Total: R${quantidade * valor:.2f}\n")
            arquivo.write(f"Data e Hora: {data_hora}\n")
            arquivo.write(f"Local da Compra: {local}\n")
            arquivo.write("Obrigado pela compra!\n")

def gerar_nota_fiscal_pdf(nome, quantidade, valor, local, nota_fiscal=None):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if nota_fiscal is None:
        nota_fiscal = str(uuid.uuid4())[3:11]  # Gerar número único da nota fiscal sem os três primeiros caracteres
    default_filename = f"NotaFiscal_{nota_fiscal}.pdf"
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=default_filename, filetypes=[("PDF files", "*.pdf")])
    if file_path:
        c = canvas.Canvas(file_path)
        c.drawString(100, 750, f"Nota Fiscal: {nota_fiscal}")
        c.drawString(100, 730, f"Produto: {nome}")
        c.drawString(100, 710, f"Quantidade: {quantidade}")
        c.drawString(100, 690, f"Valor Unitário: R${valor:.2f}")
        c.drawString(100, 670, f"Valor Total: R${quantidade * valor:.2f}")
        c.drawString(100, 650, f"Data e Hora: {data_hora}")
        c.drawString(100, 630, f"Local da Compra: {local}")
        c.drawString(100, 610, "Obrigado pela compra!")
        c.save()