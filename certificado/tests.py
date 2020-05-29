from django.contrib.auth.models import User, Group
from django.test import RequestFactory, Client, TransactionTestCase
from django.urls import reverse

from certificado.models import Certificado, make_slug


class CertificadoTestCase(TransactionTestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

        # Staff user
        self.user_staff = User.objects.create_user(username='jacob',
                                                   email='jacob@…',
                                                   password='top_secret')
        self.group = Group.objects.create(name='Testes')
        self.group.user_set.add(self.user_staff)

        self.certificado = Certificado.objects.create(aluno='Aluno Teste',
                                                      curso='Curso Teste',
                                                      carga_horaria='2',
                                                      data='2020-04-23',
                                                      parceria=1,
                                                      modalidade=1,
                                                      slug=make_slug())

    def teste_view_certificados_logado(self):
        self.client.force_login(self.user_staff)
        request = self.client.get(reverse('lista_certificados'))

        self.assertEqual(request.status_code, 200)

    def teste_view_certificados_anonimo(self):
        self.client.logout()
        request = self.client.get(reverse('lista_certificados'))

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request,
                             '/accounts/login/?next=/certificados/',
                             status_code=302,
                             target_status_code=200)

    def teste_view_certificado_download_status_code(self):
        self.client.logout()
        request = self.client.get(reverse('download_certificado',
                                          kwargs={
                                              'pk': self.certificado.pk,
                                              'slug': self.certificado.slug}))

        self.assertEqual(request.status_code, 200)

    def teste_view_certificado_novo_logado(self):
        self.client.force_login(self.user_staff)
        request = self.client.get(reverse('novo_certificado'))

        self.assertEqual(request.status_code, 200)

    def teste_view_certificado_novo_anonimo(self):
        self.client.logout()
        request = self.client.get(reverse('novo_certificado'))

        self.assertEqual(request.status_code, 302)
        self.assertRedirects(request,
                             '/accounts/login/?next=/certificado/novo/',
                             status_code=302,
                             target_status_code=200)

    def teste_novo_certificado_cadastro(self):
        certificados = Certificado.objects.all()
        self.assertEqual(len(certificados), 1)
        self.assertEqual(Certificado.objects.count(), 1)

        novo_certificado = {
            'aluno': 'Novo Aluno Teste',
            'curso': 'Curso Teste',
            'carga_horaria': '2',
            'data': '2020-04-23',
            'parceria': '1',
            'modalidade': '1',
        }

        self.client.force_login(self.user_staff)

        response = self.client.post(reverse('novo_certificado'),
                                    data=novo_certificado)
        self.assertEqual(response.status_code, 302)

        certificados = Certificado.objects.all()
        self.assertEqual(len(certificados), 2)
        self.assertEqual(Certificado.objects.count(), 2)
