# Generated by Django 2.0.5 on 2018-10-03 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0014_auto_20181003_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trouble',
            old_name='processer',
            new_name='processor',
        ),
    ]