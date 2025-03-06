from reportlab.pdfgen import canvas

def gerar_nota_fiscal_txt(nome, quantidade, nota_fiscal):
    with open(f"NotaFiscal_{nota_fiscal}.txt", "w") as arquivo:
        arquivo.write(f"Nota Fiscal: {nota_fiscal}\n")
        arquivo.write(f"Produto: {nome}\n")
        arquivo.write(f"Quantidade: {quantidade}\n")
        arquivo.write("Obrigado pela compra!\n")

def gerar_nota_fiscal_pdf(nome, quantidade, nota_fiscal):
    c = canvas.Canvas(f"NotaFiscal_{nota_fiscal}.pdf")
    c.drawString(100, 750, f"Nota Fiscal: {nota_fiscal}")
    c.drawString(100, 730, f"Produto: {nome}")
    c.drawString(100, 710, f"Quantidade: {quantidade}")
    c.drawString(100, 690, "Obrigado pela compra!")
    c.save()
