# Generated by Django 5.1.5 on 2025-03-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_worker_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='amount',
            field=models.TextField(),
        ),
    ]
