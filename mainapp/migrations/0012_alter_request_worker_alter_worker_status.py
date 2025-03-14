# Generated by Django 5.1.5 on 2025-03-12 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_alter_user_email_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='mainapp.worker'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Not Available', 'Not Available')], default='Available', max_length=20),
        ),
    ]
