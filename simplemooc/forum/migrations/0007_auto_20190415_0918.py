# Generated by Django 2.1.7 on 2019-04-15 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20190415_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'simplemooc.forum'), ('model', 'Thread')), models.Q(('app_label', 'simplemooc.forum'), ('model', 'Comment')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
