# Generated by Django 2.1.7 on 2019-04-16 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20190415_1721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='replies',
            new_name='answers',
        ),
    ]
