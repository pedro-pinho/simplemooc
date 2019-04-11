from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.core import mail
from django.conf import settings

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from simplemooc.courses.models import Course, Announcement
from simplemooc.accounts.models import User

class CourseManagerTestCase(TestCase):
    
    def setUp(self):
        self.courses_django = mommy.make('courses.Course', name='django', _quantity=5)
        self.courses_devs = mommy.make('courses.Course', name='devs', _quantity=5)
        self.client = Client()

    def tearDown(self):
        del self.courses_django
        del self.courses_devs

    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 5)

# @todo: Enrollment