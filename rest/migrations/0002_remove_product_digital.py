# Generated by Django 5.0.1 on 2024-01-16 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]