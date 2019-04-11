# Generated by Django 2.1.7 on 2019-04-07 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_announcement_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('number', models.IntegerField(blank=True, default=0, verbose_name='Número (ordem)')),
                ('release_date', models.DateField(blank=True, null=True, verbose_name='Disponível em')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.Course', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Aula',
                'verbose_name_plural': 'Aulas',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('embedded', models.TextField(blank=True, verbose_name='Video')),
                ('file', models.FileField(blank=True, null=True, upload_to='lessons/materials/', verbose_name='Material')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='courses.Lesson', verbose_name='Lição')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.Lesson', verbose_name='Lição')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiais',
                'ordering': ['created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ['-created_at'], 'verbose_name': 'Anúncio', 'verbose_name_plural': 'Anúncios'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at'], 'verbose_name': 'Comentário', 'verbose_name_plural': 'Comentários'},
        ),
    ]
