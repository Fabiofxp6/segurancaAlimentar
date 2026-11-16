from io import BytesIO

from django.core.exceptions import ValidationError
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .campo_arquivos import ler_arquivo, metadados_arquivo, tipo_imagem


def _validar_pdf(conteudo):
    try:
        with PdfReader(BytesIO(conteudo), strict=True) as pdf:
            if pdf.is_encrypted:
                raise ValidationError("Envie um PDF sem senha.")
            paginas_declaradas = pdf.root_object["/Pages"]["/Count"]
            if not 1 <= paginas_declaradas <= 50 or not 1 <= len(pdf.pages) <= 50:
                raise ValidationError("Envie um PDF de 1 a 50 páginas.")
    except (PdfReadError, OSError, ValueError, TypeError, KeyError, RecursionError, IndexError) as erro:
        raise ValidationError("Selecione um documento PDF válido.") from erro


def validar_documento(arquivo):
    conteudo = ler_arquivo(arquivo, "Envie um documento de até 5 MiB.")
    if conteudo.startswith(b"%PDF-"):
        _validar_pdf(conteudo)
        mime, extensao = "application/pdf", ".pdf"
    else:
        mime, extensao = tipo_imagem(conteudo)
    return metadados_arquivo(arquivo.name, conteudo, mime, extensao), conteudo
