# Generated by Django 2.1.7 on 2019-04-14 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20190414_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='forum.Thread', verbose_name='thread'),
        ),
    ]