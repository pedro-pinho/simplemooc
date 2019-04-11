from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.core import mail
from django.conf import settings
from django.test import RequestFactory, TestCase

from simplemooc.courses.models import Course, Announcement, Enrollment

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

class ContactCourseTestCase(TestCase):

    def setUp(self):
        
        self.course = mommy.make('courses.Course', _quantity=1)

        self.client = Client()

    def tearDown(self):
        del self.course
    #antes de cada função, o django chama setup e depois que ele terminou, o tearDown

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_contact_form_error(self):
        data = {'name': 'Fulano de tal'}
        client = Client()
        path = reverse('courses:details', args=[self.course[0].slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form','email','Este campo é obrigatório.')
        self.assertFormError(response, 'form','message','Este campo é obrigatório.')

    def test_contact_form_success(self):
        data = {'name': 'Fulano de tal', 'email':'fulano@gmail.com', 'message':'Gostei! Mas, o que eu faço da vida?' }
        client = Client()
        path = reverse('courses:details', args=[self.course[0].slug])
        response = client.post(path, data)
        self.assertEqual(response.status_code, 200) #nao deu erro no formulário
        self.assertEqual(len(mail.outbox),1) #enviou o email
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL]) #pra pessoa certa


class EnrollTestCase(TestCase):
    # self.user = mommy.make('accounts.User', 
    #     username='admin',
    #     is_active = True,
    #     is_staff=True)
    # self.user.set_password('admin123')
    # self.user.save()
    # self.client.login(username='admin', password='admin123')
    def setUp(self):
        self.user = mommy.make('accounts.User', 
            username='Megan',
            is_active = True)
        self.user.set_password('password')
        self.user.save()

        self.course = mommy.make('courses.Course', slug='django', _quantity=1)
        self.announcements = mommy.make('courses.Announcement', _quantity=5)
        #self.course[0].announcements.set(self.announcement[:])
        
        self.client = Client()

    def tearDown(self):
        del self.user
        del self.course
        del self.announcements

    def test_enrollment_error(self):
        self.client.login(username='Megan', password='password')
        path = reverse('courses:enrollment', args=['abobrinha'])
        response = self.client.post(path)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_enrollment_success(self):
        self.client.login(username='Megan', password='password')
        path = reverse('courses:enrollment', args=[self.course[0].slug])
        response = self.client.post(path)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_undo_enrollment_error(self):
        self.client.login(username='Megan', password='password')
        path = reverse('courses:undo_enrollment', args=[self.course[0].slug])
        response = self.client.post(path)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_undo_enrollment_success(self):
        self.client.login(username='Megan', password='password')
        path = reverse('courses:enrollment', args=[self.course[0].slug])
        response = self.client.post(path)
        # self.course[0].announcements.set(self.announcements[:])

        path = reverse('courses:undo_enrollment', args=[self.course[0].slug])
        response = self.client.post(path)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_comment_annoncement_form_error_blank(self):
        data = {'comment': ''}
        self.client.login(username='Megan', password='password')

        path = reverse('courses:enrollment', args=[self.course[0].slug])
        response = self.client.post(path, {})
        self.course[0].announcements.set(self.announcements[:])
        path = reverse('courses:announcement_detail', args=[self.course[0].slug, self.course[0].announcements.first().id])
        response = self.client.post(path, data)
        self.assertFormError(response, 'form','comment','Este campo é obrigatório.')
        self.client.logout()
        
    def test_comment_annoncement_form_error_no_login(self):
        data = {'comment': 'Muito bom esse anuncio!'}
        path = reverse('courses:enrollment', args=[self.course[0].slug])
        response = self.client.post(path, data)
        self.course[0].announcements.set(self.announcements[:])

        path = reverse('courses:announcement_detail', args=[self.course[0].slug, self.course[0].announcements.first().id])
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 302)
        
    def test_comment_annoncement_form_success(self):
        data = {'comment': 'Muito legal isso!'}
        self.client.login(username='Megan', password='password')
        path = reverse('courses:enrollment', args=[self.course[0].slug])
        self.client.post(path)
        self.course[0].announcements.set(self.announcements[:])

        path = reverse('courses:announcement_detail', args=[self.course[0].slug, self.course[0].announcements.first().id])
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()


class AnnouncementsTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make('accounts.User', 
            username='Megan',
            is_active = True)
        self.user.set_password('password')
        self.user.save()

        self.course = mommy.make('courses.Course', _quantity=1)
        self.announcements = mommy.make('courses.Announcement', _quantity=5)
        self.enrollment = mommy.make('courses.Enrollment', _quantity=5)

        self.client = Client()

    def tearDown(self):
        del self.course
        del self.announcements
        del self.enrollment

    def test_announcements_index(self):
        self.client.login(username='Megan', password='password')
        path = reverse('courses:enrollment', args=[self.course[0].slug])
        self.client.post(path)
        self.course[0].announcements.set(self.announcements[:])

        response = self.client.get(reverse('courses:announcements',args=[self.course[0].slug]))
        self.assertTemplateUsed(response, 'courses/announcements.html')
        self.assertTemplateUsed(response, 'courses/course_dashboard.html')
        self.assertTemplateUsed(response, 'accounts/dashboard.html')