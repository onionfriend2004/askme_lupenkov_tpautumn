# Generated by Django 5.1.2 on 2024-12-25 07:07

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_question_search'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='question',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search'], name='app_questio_search_04f5d6_gin'),
        ),
    ]
