from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

# Durante os testes, o Django cria um banco novo: nome_do_banco_principal_test
# Precisa garantir que o usuário que foi configurado no settings tem permissão pra criar novos bancos de dados
# Nesse caso, o SQLite permite qualquer usuario a criar banco

# https://docs.djangoproject.com/en/2.1/topics/testing/overview/

# por padrão, o django executa as funções que tem nome "test_xxx"
class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_status_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        client = Client()
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_template_contact_used(self):
        client = Client()
        response = self.client.get(reverse('core:contact'))
        self.assertTemplateUsed(response, 'contact.html')