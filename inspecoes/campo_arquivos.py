from hashlib import sha256
from io import BytesIO
from pathlib import PurePath

from django.core.exceptions import ValidationError
from PIL import Image


LIMITE_BYTES = 5 * 1024 * 1024
LIMITE_PIXELS = 20_000_000
LIMITE_NOME = 160
FORMATOS = {"JPEG": ("image/jpeg", ".jpg"), "PNG": ("image/png", ".png")}


def ler_arquivo(arquivo, mensagem):
    if not 0 < arquivo.size <= LIMITE_BYTES:
        raise ValidationError({"arquivo": mensagem})
    conteudo = arquivo.read(LIMITE_BYTES + 1)
    if len(conteudo) != arquivo.size:
        raise ValidationError({"arquivo": "O arquivo recebido está incompleto."})
    return conteudo


def metadados_arquivo(nome_original, conteudo, mime, extensao):
    base = PurePath(nome_original.replace("\\", "/")).stem
    base = "".join(caractere for caractere in base if caractere.isprintable()).strip(" .")
    nome = (base[:LIMITE_NOME - len(extensao)] or "evidencia") + extensao
    return {"nome": nome, "mime": mime, "tamanho": len(conteudo), "sha256": sha256(conteudo).hexdigest()}


def tipo_imagem(conteudo):
    try:
        with Image.open(BytesIO(conteudo), formats=list(FORMATOS)) as imagem:
            if imagem.width * imagem.height > LIMITE_PIXELS or getattr(imagem, "is_animated", False):
                raise ValidationError({"arquivo": "Envie uma imagem estática de até 20 megapixels."})
            formato = imagem.format
            imagem.verify()
        with Image.open(BytesIO(conteudo), formats=[formato]) as imagem:
            imagem.load()
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError) as erro:
        raise ValidationError({"arquivo": "Selecione uma imagem JPEG ou PNG válida."}) from erro
    return FORMATOS[formato]


def validar_arquivo(arquivo):
    conteudo = ler_arquivo(arquivo, "Envie uma imagem de até 5 MiB.")
    mime, extensao = tipo_imagem(conteudo)
    return metadados_arquivo(arquivo.name, conteudo, mime, extensao), conteudo
