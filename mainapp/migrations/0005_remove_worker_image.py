# Generated by Django 5.1.5 on 2025-02-23 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_rename_skills_worker_profession'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='image',
        ),
    ]
