# Generated by Django 5.0.3 on 2025-01-04 10:20

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdapp', '0006_remove_sequence_desc_explicit_formula_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interpretation',
            name='example_image',
        ),
        migrations.RemoveField(
            model_name='interpretation',
            name='example_table',
        ),
        migrations.RemoveField(
            model_name='interpretation',
            name='example_text',
        ),
        migrations.AlterField(
            model_name='interpretation',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(max_length=500, verbose_name='Описание'),
        ),
    ]
