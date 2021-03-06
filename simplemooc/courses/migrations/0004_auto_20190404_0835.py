# Generated by Django 2.1.7 on 2019-04-04 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simplemooc.core.enums


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_auto_20190329_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[(simplemooc.core.enums.Status_Course('Pendente'), 'Pendente'), (simplemooc.core.enums.Status_Course('Aprovado'), 'Aprovado'), (simplemooc.core.enums.Status_Course('Cancelado'), 'Cancelado'), (simplemooc.core.enums.Status_Course('Inscrito'), 'Inscrito')], default=simplemooc.core.enums.Status_Course('Pendente'), max_length=2, verbose_name='Situação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.Course', verbose_name='Curso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
            },
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('user', 'course')},
        ),
    ]
