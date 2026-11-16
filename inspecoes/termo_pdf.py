from html import escape
from io import BytesIO

from django.utils import timezone
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


VERDE = HexColor("#18564B")
TEXTO = HexColor("#19332E")
NEUTRO = HexColor("#45645D")
FUNDO = HexColor("#EAF3F0")
MARGEM = 48


def _texto(valor):
    return escape(" ".join(str(valor).split()))


def _data(instante):
    return timezone.localtime(instante).strftime("%d/%m/%Y %H:%M %Z")


def _rodape(canvas, documento):
    largura, altura = A4
    canvas.setFillColor(VERDE)
    canvas.rect(0, altura - 6, largura, 6, fill=1, stroke=0)
    canvas.setStrokeColor(FUNDO)
    canvas.line(MARGEM, 45, largura - MARGEM, 45)
    canvas.setFillColor(NEUTRO)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(MARGEM, 29, "Documento de demonstração")
    canvas.drawRightString(largura - MARGEM, 29, f"Página {documento.page}")


def gerar(resultado, *, codigo, versao, emitido_em, itens, anterior_codigo=None):
    inspecao = resultado.inspecao
    unidade = inspecao.identificacao_estabelecimento
    checklist = resultado.versao_checklist
    corpo = ParagraphStyle("Corpo", fontName="Helvetica", fontSize=10.5, leading=15, textColor=TEXTO,
                           spaceAfter=7, alignment=TA_LEFT)
    titulo = ParagraphStyle("Título", parent=corpo, fontName="Helvetica-Bold", fontSize=26,
                            leading=30, textColor=VERDE, spaceAfter=11)
    secao = ParagraphStyle("Seção", parent=corpo, fontName="Helvetica-Bold", fontSize=13, leading=17,
                           textColor=VERDE, spaceBefore=12, spaceAfter=7, keepWithNext=True)
    item_titulo = ParagraphStyle("Item", parent=corpo, fontName="Helvetica-Bold", keepWithNext=True)
    info = ParagraphStyle("Info", parent=corpo, fontSize=9, leading=13, textColor=NEUTRO, spaceAfter=9)
    resultado_visual = ParagraphStyle("Resultado", parent=corpo, fontName="Helvetica-Bold",
                                      fontSize=17, leading=23, backColor=FUNDO, borderPadding=10,
                                      spaceBefore=16, spaceAfter=12)

    nota = resultado.pontuacao
    classificacao = resultado.get_classificacao_display()
    linha_resultado = classificacao if nota is None else f"{nota:.2f}% · {classificacao}".replace(".", ",")
    secoes = [
        Paragraph("SISTEMA DE AVALIAÇÃO DE SEGURANÇA ALIMENTAR", info),
        Paragraph("Termo retificador" if anterior_codigo else "Termo de inspeção", titulo),
        Paragraph(f"{_texto(codigo)} · Versão {versao} · Demonstração", info),
        Paragraph("Identificação da inspeção", secao),
        Paragraph(f"<b>Estabelecimento</b> {_texto(unidade['nome'])}", corpo),
    ]
    if anterior_codigo:
        secoes.insert(3, Paragraph(
            f"Retifica {_texto(anterior_codigo)} após correção autorizada da avaliação.", info,
        ))
    if unidade.get("documento"):
        secoes.append(Paragraph(f"<b>Documento cadastral</b> {_texto(unidade['documento'])}", corpo))
    secoes.extend([
        Paragraph(f"<b>Inspeção</b> #{inspecao.pk} · Concluída em {_data(resultado.concluido_em)}", corpo),
        Paragraph(f"<b>Checklist</b> {_texto(checklist.titulo)} · Versão {checklist.numero}", corpo),
        Paragraph(f"<b>Emissão</b> {_data(emitido_em)}", corpo),
        Paragraph("Resultado da avaliação", secao),
        Paragraph(_texto(linha_resultado), resultado_visual),
        Spacer(1, 4),
        Paragraph("Itens não conformes e irregularidades", secao),
    ])
    if not itens:
        secoes.append(Paragraph("Nenhum item não conforme ou irregularidade registrada.", corpo))
    for ordem, enunciado, nao_conforme, descricao in itens:
        qualificacao = "Não conforme" if nao_conforme else "Irregularidade registrada"
        texto = f"{ordem}. {_texto(enunciado)} · {qualificacao}"
        secoes.append(Paragraph(texto, item_titulo if descricao else corpo))
        if descricao:
            secoes.append(Paragraph(f"<b>Irregularidade</b> {_texto(descricao)}", corpo))

    saida = BytesIO()
    documento = SimpleDocTemplate(
        saida, pagesize=A4, title=f"Termo {codigo} - Demonstração",
        leftMargin=MARGEM, rightMargin=MARGEM, topMargin=48, bottomMargin=63,
        author="Sistema de Avaliação de Segurança Alimentar",
    )
    documento.build(secoes, onFirstPage=_rodape, onLaterPages=_rodape)
    return saida.getvalue()
