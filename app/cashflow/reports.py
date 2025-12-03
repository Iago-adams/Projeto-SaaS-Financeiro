import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

# Importando a função que gera o OBJETO figure do Plotly
from .analysis import get_extract_figure 

def generate_cashflow_PDF(company_name, kpis, dataframe):
    """
    Gera o PDF focado em Evolução de Saldo.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4 # 595.27, 841.89
    
    # --- 0. CÁLCULOS EXTRAS PARA O PDF ---
    # Como os KPIs padrão agora retornam 0 para receita/despesa,
    # vamos calcular o Saldo Inicial e Variação direto do DataFrame aqui.
    if not dataframe.empty:
        saldo_inicial = dataframe['amount'].iloc[0]
        saldo_final = dataframe['amount'].iloc[-1]
        data_inicial = dataframe['completedAt'].iloc[0].strftime('%d/%m/%Y')
        data_final = dataframe['completedAt'].iloc[-1].strftime('%d/%m/%Y')
        variacao = saldo_final - saldo_inicial
    else:
        saldo_inicial = 0
        saldo_final = 0
        variacao = 0
        data_inicial = "--"
        data_final = "--"

    # --- 1. CABEÇALHO ---
    c.setTitle(f"Extrato - {company_name}")
    
    # Título Principal
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor('#333333'))
    c.drawString(40, height - 50, f"Relatório de Saldo: {company_name}")
    
    # Data de Geração
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#666666'))
    c.drawString(40, height - 70, f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    c.drawString(40, height - 85, f"Período analisado: {data_inicial} até {data_final}")
    
    # --- 2. CAIXAS DE RESUMO (MÉTRICAS) ---
    y_cards = height - 140
    card_width = (width - 80) / 3 # Divide largura em 3 colunas
    
    # Função auxiliar para desenhar cards
    def draw_card(x, title, value, value_color='#000000', subtext=""):
        # Fundo do card
        c.setFillColor(HexColor('#f9f9f9'))
        c.roundRect(x, y_cards, card_width - 10, 60, 8, fill=True, stroke=False)
        
        # Título
        c.setFillColor(HexColor('#666666'))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 10, y_cards + 45, title)
        
        # Valor
        c.setFillColor(HexColor(value_color))
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 10, y_cards + 25, f"R$ {value:,.2f}")
        
        # Subtexto (opcional)
        if subtext:
            c.setFillColor(HexColor('#999999'))
            c.setFont("Helvetica", 8)
            c.drawString(x + 10, y_cards + 10, subtext)

    # CARD 1: Saldo Inicial
    draw_card(40, "Saldo Inicial", saldo_inicial, '#333333', "Início do período")
    
    # CARD 2: Variação (Verde se subiu, Vermelho se desceu)
    cor_var = '#2E8B57' if variacao >= 0 else '#CD5C5C'
    sinal = "+" if variacao >= 0 else ""
    draw_card(40 + card_width, "Variação no Período", variacao, cor_var, f"{sinal}R$ {variacao:,.2f}")
    
    # CARD 3: Saldo Final
    cor_final = '#000000' if saldo_final >= 0 else '#FF0000'
    draw_card(40 + (card_width * 2), "Saldo Final", saldo_final, cor_final, "Saldo atual")

    # --- 3. GRÁFICO (Imagem) ---
    # Reutiliza sua lógica do analysis.py para criar a figura
    # O gráfico agora é de Área (Saldo), que combina com esse relatório
    fig = get_extract_figure(dataframe)
    
    # Converte figura para bytes (PNG)
    # Aumentei scale para 3 para ficar com alta resolução no PDF
    img_bytes = fig.to_image(format="png", engine="kaleido", scale=3, width=800, height=450)
    
    # Coloca no PDF
    imagem = ImageReader(io.BytesIO(img_bytes))
    img_w, img_h = imagem.getSize()
    aspect = img_h / float(img_w)
    display_width = width - 80
    display_height = display_width * aspect
    
    # Posiciona a imagem abaixo dos cards
    c.drawImage(imagem, 40, y_cards - 20 - display_height, width=display_width, height=display_height, mask='auto')
    
    # Rodapé
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor('#cccccc'))
    c.drawCentredString(width / 2, 30, f"Documento gerado automaticamente por {company_name} SaaS Financeiro")
    
    # Finaliza
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()