import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

# Importando a função que gera o OBJETO figure do Plotly (reutilização)
from .analysis import get_extract_figure 

def generate_cashflow_PDF(company_name, kpis, dataframe):
    """
    Gera o PDF com Extrato Gráfico e KPIs.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4 # 595.27, 841.89
    
    # --- 1. CABEÇALHO ---
    c.setTitle(f"Extrato - {company_name}")
    
    # Título
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor('#333333'))
    c.drawString(40, height - 50, f"Relatório Financeiro: {company_name}")
    
    # Data
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#666666'))
    c.drawString(40, height - 70, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    
    # --- 2. KPIS (Resumo) ---
    y_kpi = height - 120
    c.setFillColor(HexColor('#f5f5f5')) # Fundo cinza box
    c.rect(40, y_kpi - 10, width - 80, 50, fill=True, stroke=False)
    
    c.setFillColor(HexColor('#000000'))
    c.setFont("Helvetica-Bold", 10)
    
    # Receita
    c.drawString(60, y_kpi + 25, "Receita Total")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#2E8B57')) # Verde
    c.drawString(60, y_kpi + 10, f"R$ {kpis.get('total_revenue', 0):,.2f}")
    
    # Despesas
    c.setFillColor(HexColor('#000000'))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(220, y_kpi + 25, "Despesas Totais")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#CD5C5C')) # Vermelho
    c.drawString(220, y_kpi + 10, f"R$ {kpis.get('total_expenses', 0):,.2f}")
    
    # Saldo
    c.setFillColor(HexColor('#000000'))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(380, y_kpi + 25, "Saldo Atual")
    c.setFont("Helvetica", 12)
    saldo = kpis.get('current_balance', 0)
    c.setFillColor(HexColor('#000000') if saldo >= 0 else HexColor('#FF0000'))
    c.drawString(380, y_kpi + 10, f"R$ {saldo:,.2f}")

    # --- 3. GRÁFICO (Imagem) ---
    # Reutiliza sua lógica do analysis.py para criar a figura
    fig = get_extract_figure(dataframe)
    
    # Converte figura para bytes (PNG) usando Kaleido
    img_bytes = fig.to_image(format="png", engine="kaleido", scale=2, width=800, height=450)
    
    # Coloca no PDF
    imagem = ImageReader(io.BytesIO(img_bytes))
    img_w, img_h = imagem.getSize()
    aspect = img_h / float(img_w)
    display_width = width - 80
    display_height = display_width * aspect
    
    c.drawImage(imagem, 40, y_kpi - 40 - display_height, width=display_width, height=display_height, mask='auto')
    
    # Finaliza
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()