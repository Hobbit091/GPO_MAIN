# Generated by Django 5.0.3 on 2024-11-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdapp', '0005_algorithm_alg_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sequence_desc',
            name='explicit_formula',
        ),
        migrations.RemoveField(
            model_name='sequence_desc',
            name='generating_function',
        ),
        migrations.RemoveField(
            model_name='sequence_desc',
            name='other_formula',
        ),
    ]