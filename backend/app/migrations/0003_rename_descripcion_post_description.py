# Generated by Django 4.2.3 on 2024-05-01 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='descripcion',
            new_name='description',
        ),
    ]
