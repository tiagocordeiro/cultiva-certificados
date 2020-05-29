from django.forms import ModelForm, TextInput, Select, DateInput

from .models import Certificado


class CertificadoForm(ModelForm):
    class Meta:
        model = Certificado
        fields = [
            'aluno',
            'universidade',
            'rg',
            'cpf',
            'curso',
            'modalidade',
            'carga_horaria',
            'data',
            'parceria',
        ]

        widgets = {
            'aluno': TextInput(attrs={'class': 'form-control'}),
            'universidade': TextInput(attrs={'class': 'form-control'}),
            'rg': TextInput(attrs={'class': 'form-control'}),
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'curso': TextInput(attrs={'class': 'form-control'}),
            'modalidade': Select(attrs={'class': 'form-control'}),
            'carga_horaria': TextInput(attrs={'class': 'form-control'}),
            'data': DateInput(attrs={'class': 'form-control'}),
            'parceria': Select(attrs={'class': 'form-control'}),
        }
