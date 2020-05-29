import locale
import os

from PIL import Image, ImageDraw, ImageFont
from django.utils.text import slugify

from certgen import settings
from .models import Certificado

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gera_certificado(pk, slug):
    templates_dir = os.path.abspath(settings.BASE_DIR + '/templates/modelos/')
    certificado = Certificado.objects.get(pk=pk, slug=slug)

    if certificado.parceria == 1:
        modelo = 'certificado_parceiro_atens'
    elif certificado.parceria == 2:
        modelo = 'certificado_parceiro_flacso'
    else:
        modelo = 'certificado_base'

    certificado.image = Image.open(f'{templates_dir}/{modelo}.png')
    draw = ImageDraw.Draw(certificado.image)
    certificado.date_string = certificado.data.strftime("%d de %B de %Y")

    font_title = ImageFont.truetype(f'{templates_dir}/fontes/title.ttf', 48)
    font_body = ImageFont.truetype(f'{templates_dir}/fontes/body.ttf', 42)

    tamanho_data = draw.textsize(certificado.date_string, font=font_title)

    draw.text(
        (1300, 1100),
        text=certificado.aluno,
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1200),
        text=f'RG: {certificado.rg}',
        fill='#3A317B',
        font=font_body
    )

    draw.text(
        (1300, 1300),
        text=certificado.curso,
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1400),
        text=certificado.get_modalidade_display(),
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1520),
        text=f'{certificado.carga_horaria} horas',
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1620 - tamanho_data[0], 2020),
        text=f'{certificado.date_string}.',
        align='right',
        fill='#3A317B',
        font=font_title
    )

    certificado.file_name = gen_file_name(certificado.aluno)

    return certificado


def gen_file_name(text: str):
    return slugify(text)
