# Generated by Django 4.1.13 on 2024-04-22 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['id']},
        ),
    ]
