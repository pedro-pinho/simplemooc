from django.template import Library
from simplemooc.courses.models import Enrollment

from simplemooc.core.enums import Status_Course

register = Library()

@register.inclusion_tag('templatetags/my_courses.html') #opção 1: força o html direto na pagina
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user).exclude(status=Status_Course.CAN)
    context = {
        'enrollments': enrollments
    }
    return context
@register.simple_tag # opção 2: carrega uma variável, permitindo o uso de qualquer forma. Recomendável
def load_my_courses(user):
    return Enrollment.objects.filter(user=user).exclude(status=Status_Course.CAN)