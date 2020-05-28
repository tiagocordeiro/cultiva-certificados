import uuid

from django.db import models

from core.models import Active, TimeStampedModel


def make_slug():
    return str(uuid.uuid4())


class Certificado(Active, TimeStampedModel):
    PARCERIA_CHOICES = (
        (1, 'ATENS'),
        (2, 'FLACSO'),
        (3, 'Prefeitura de Suzano'),
    )

    aluno = models.CharField('Aluno', max_length=100)
    universidade = models.CharField('Universidade', max_length=50, blank=True)
    rg = models.CharField('RG', max_length=15, blank=True)
    cpf = models.CharField('CPF', max_length=15, blank=True)
    curso = models.TextField('Curso')
    carga_horaria = models.IntegerField('Carga horária')
    data = models.DateField('Data')
    parceria = models.IntegerField('Parceria', choices=PARCERIA_CHOICES)
    slug = models.UUIDField(unique=True, editable=False)

    class Meta:
        ordering = ('data', 'curso', 'aluno',)
        verbose_name_plural = "certificados"
        verbose_name = "certificado"

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = make_slug()
            super(Certificado, self).save(*args, **kwargs)
        super(Certificado, self).save(*args, **kwargs)
