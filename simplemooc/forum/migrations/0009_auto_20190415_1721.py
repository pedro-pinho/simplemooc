# Generated by Django 2.1.7 on 2019-04-15 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20190415_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Atalho'),
        ),
    ]