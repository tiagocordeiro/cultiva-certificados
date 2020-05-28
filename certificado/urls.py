from django.urls import path

from . import views

urlpatterns = [
    path('certificados/', views.lista_certificados, name='lista_certificados'),
    path('certificado/novo/', views.novo_certificado, name='novo_certificado'),
    path('certificado/editar/<pk>/', views.atualiza_certificado,
         name='atualiza_certificado'),
    path('certificado/compartilhar/<pk>/', views.compartilha_certificado,
         name='compartilhar_certificado'),
    path('certificado/<pk>/<slug>/', views.link_certificado,
         name='link_certificado'),
    path('certificado/download/<pk>/<slug>/', views.download_certificado,
         name='download_certificado'),
    path('certificado/download/<pk>/<slug>/<img_format>',
         views.download_certificado,
         name='download_certificado_png')
]
