import csv
import io
import locale
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont
from django.utils.text import slugify

from certgen import settings
from .models import Certificado, make_slug

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def gera_certificado(pk, slug):
    templates_dir = os.path.abspath(settings.BASE_DIR + '/templates/modelos/')
    certificado = Certificado.objects.get(pk=pk, slug=slug)
    two_signtures = False

    if certificado.parceria == 1:
        modelo = 'certificado_parceiro_atens'
    elif certificado.parceria == 2:
        modelo = 'certificado_parceiro_flacso'
    elif certificado.parceria == 4:
        modelo = 'certificado_parceiro_atens_dir_rosario'
        two_signtures = True
    else:
        modelo = 'certificado_base'

    certificado.image = Image.open(f'{templates_dir}/{modelo}.png')
    draw = ImageDraw.Draw(certificado.image)
    certificado.date_string = certificado.data.strftime("%d de %B de %Y")

    font_title = ImageFont.truetype(f'{templates_dir}/fontes/title.ttf', 48)
    # font_body = ImageFont.truetype(f'{templates_dir}/fontes/body.ttf', 42)

    tamanho_data = draw.textsize(certificado.date_string, font=font_title)

    texto = certificado.curso
    if len(texto) > 50:
        linhas = textwrap.wrap(texto, 50)

    else:
        linhas = [texto, certificado.get_modalidade_display()]

    draw.text(
        (1300, 1100),
        text=certificado.aluno,
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1190),
        text=f'RG: {certificado.rg}',
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1300),
        text=linhas[0],
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1400),
        text=linhas[1],
        fill='#3A317B',
        font=font_title
    )

    draw.text(
        (1300, 1520),
        text=f'{certificado.carga_horaria} horas',
        fill='#3A317B',
        font=font_title
    )

    if two_signtures:
        draw.text(
            (1250 - tamanho_data[0], 2020),
            text=f'{certificado.date_string}.',
            align='right',
            fill='#3A317B',
            font=font_title
        )
    else:
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


def data_from_csv(csv_file):
    csv_file = io.TextIOWrapper(csv_file)
    dialect = csv.Sniffer().sniff(csv_file.read(1024), delimiters=";,")
    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect)
    return list(reader)


def import_certificados(lista: list):
    certificados_novos = []
    certificados_existentes = []

    for certificado in lista[1:]:
        if Certificado.objects.filter(aluno__exact=certificado[0],
                                      curso__exact=certificado[4]):
            certificados_existentes.append(
                {'aluno': certificado[0],
                 'curso': certificado[4]}
            )
        else:
            novo_certificado = Certificado(aluno=certificado[0],
                                           universidade=certificado[1],
                                           rg=certificado[2],
                                           cpf=certificado[3],
                                           curso=certificado[4],
                                           modalidade=certificado[5],
                                           carga_horaria=certificado[6],
                                           data=certificado[7],
                                           parceria=certificado[8],
                                           slug=make_slug())
            certificados_novos.append(novo_certificado)

    if len(certificados_novos) >= 1:
        Certificado.objects.bulk_create(certificados_novos)

    return {'novos': certificados_novos, 'existentes': certificados_existentes}
