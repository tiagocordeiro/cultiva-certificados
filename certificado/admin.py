from django.contrib import admin

# Register your models here.
from .models import Certificado


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'parceria', 'data')
    list_filter = ('curso', 'parceria')


admin.site.register(Certificado, CertificadoAdmin)
