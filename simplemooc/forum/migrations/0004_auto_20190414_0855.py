# Generated by Django 2.1.7 on 2019-04-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20190414_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Título'),
        ),
    ]
