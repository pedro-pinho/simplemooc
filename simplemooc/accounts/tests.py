from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

class LoginViewTest(TestCase):
    def test_login_status_code(self):
        client = Client()
        response = client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_no_login(self):
        client = Client()
        response = client.get(reverse('accounts:dashboard'))
        self.assertNotEqual(response.status_code, 200)

class DashboardViewTest(TestCase):
    def test_dashboard_no_login(self):
        client = Client()
        response = client.get(reverse('accounts:dashboard'))
        self.assertNotEqual(response.status_code, 200)