# Generated by Django 2.0.5 on 2018-09-25 14:06

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='detail',
            field=tinymce.models.HTMLField(verbose_name='正文'),
        ),
    ]