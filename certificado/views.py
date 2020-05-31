import csv
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import FileResponse
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.urls import reverse

from .facade import gera_certificado, data_from_csv, import_certificados
from .forms import CertificadoForm
from .models import Certificado


@login_required
def lista_certificados(request):
    todos_certificados = Certificado.objects.all()
    pagina = request.GET.get('page', 1)
    paginador = Paginator(todos_certificados, 5)
    try:
        certificados = paginador.page(pagina)
    except PageNotAnInteger:
        certificados = paginador.page(1)
    except EmptyPage:
        certificados = paginador.page(paginador.num_pages)

    contexto = {
        'certificados': certificados,
    }

    return render(request, 'certificado/certificados.html', contexto)


@login_required
def novo_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Certificado cadastrado com sucesso')
                return redirect('lista_certificados')
        except Exception as e:
            messages.warning(request, f'Ocorreu um erro ao atualizar: {e}')

    else:
        form = CertificadoForm()

    return render(request, 'certificado/cadastro.html', {'form': form})


@login_required
def atualiza_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Certificado atualizado")
                return redirect('atualiza_certificado', pk)
        except Exception as e:
            messages.warning(request, f'Ocorreu um erro ao atualizar: {e}')

    else:
        form = CertificadoForm(instance=certificado)

    return render(request, 'certificado/update.html', {'form': form})


@login_required
def compartilha_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    url = request.build_absolute_uri(reverse('link_certificado',
                                             kwargs={
                                                 'pk': certificado.pk,
                                                 'slug': certificado.slug}))

    context = {
        'certificado': certificado,
        'url': url
    }

    return render(request, 'certificado/share.html', context)


def link_certificado(request, pk, slug):
    certificado = get_object_or_404(Certificado, pk=pk, slug=slug)

    contexto = {'certificado': certificado}

    return render(request, 'certificado/public.html', context=contexto)


def download_certificado(request, pk, slug, img_format='jpg'):
    if img_format == 'png':
        img_format = ['PNG', 'png']
    else:
        img_format = ['JPEG', 'jpg']

    cert_dados = gera_certificado(pk=pk, slug=slug)
    byte = BytesIO()

    cert_dados.image.save(byte, img_format[0])
    byte.seek(0)

    filename = f'{cert_dados.file_name}-{cert_dados.data}.{img_format[1]}'

    response = FileResponse(byte, 'rb')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@login_required
def download_csv_example(request):
    certificados = Certificado.objects.all()

    response = HttpResponse(content_type='text/csv')
    content = 'attachment; filename="certificados_planilha_exemplo.csv"'
    response['Content-Disposition'] = content

    colunas = []
    for key in certificados.values('aluno', 'universidade', 'rg', 'cpf',
                                   'curso', 'modalidade', 'carga_horaria',
                                   'data', 'parceria').first().keys():
        colunas.append(key)

    writer = csv.writer(response)
    writer.writerow(colunas)

    for certificado in certificados.values('aluno', 'universidade', 'rg',
                                           'cpf', 'curso', 'modalidade',
                                           'carga_horaria', 'data',
                                           'parceria'):
        colunas = []

        for value in certificado.values():
            colunas.append(value)

        writer.writerow(colunas)

    return response


@login_required
def download_csv(request):
    certificados = Certificado.objects.all()

    response = HttpResponse(content_type='text/csv')
    content = 'attachment; filename="certificados.csv"'
    response['Content-Disposition'] = content

    colunas = []
    for key in certificados.values('id', 'aluno', 'universidade', 'rg', 'cpf',
                                   'curso', 'carga_horaria', 'data',
                                   'parceria', 'slug').first().keys():
        colunas.append(key)

    colunas.append('url_download')
    colunas[7] = 'data_emissao'

    writer = csv.writer(response)
    writer.writerow(colunas)

    for certificado in certificados.values('id', 'aluno', 'universidade', 'rg',
                                           'cpf', 'curso', 'carga_horaria',
                                           'data', 'parceria', 'slug'):
        colunas = []

        for value in certificado.values():
            colunas.append(value)

        download_url = reverse('download_certificado',
                               kwargs={'pk': certificado['id'],
                                       'slug': certificado['slug']})
        dominio_site = get_current_site(request).domain
        url = ''.join(['https://', dominio_site, download_url])
        colunas.append(url)

        parceria = Certificado.objects.get(id=certificado['id'])
        colunas[8] = parceria.get_parceria_display()

        writer.writerow(colunas)

    return response


@login_required
def upload_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        csv_file = request.FILES['myfile'].file
        csv_content = data_from_csv(csv_file)

        resultado_importacao = import_certificados(csv_content)
        messages.success(request, f"Processado {resultado_importacao}")

        contexto = {'content': csv_content,
                    'resultado_importacao': resultado_importacao}

        return render(request, 'certificado/upload_csv.html', contexto)

    return render(request, 'certificado/upload_csv.html')
