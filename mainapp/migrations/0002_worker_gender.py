# Generated by Django 5.1.5 on 2025-02-22 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='gender',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
