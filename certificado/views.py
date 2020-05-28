from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import FileResponse
from django.shortcuts import redirect, render

from .facade import gera_certificado
from .forms import CertificadoForm
from .models import Certificado


# Create your views here.
@login_required
def lista_certificados(request):
    todos_certificados = Certificado.objects.all()
    pagina = request.GET.get('page', 1)
    paginador = Paginator(todos_certificados, 10)
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
    pass


@login_required
def compartilha_certificado(request, pk):
    pass


def link_certificado(request, pk, slug):
    pass


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
