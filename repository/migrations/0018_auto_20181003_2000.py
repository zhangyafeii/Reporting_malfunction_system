# Generated by Django 2.0.5 on 2018-10-03 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0017_troubletemplate_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='troubleticket',
            name='ask_user',
        ),
        migrations.RemoveField(
            model_name='troubleticket',
            name='processor',
        ),
        migrations.DeleteModel(
            name='TroubleTicket',
        ),
    ]
