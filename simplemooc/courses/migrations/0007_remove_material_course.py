# Generated by Django 2.1.7 on 2019-04-08 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20190407_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='course',
        ),
    ]