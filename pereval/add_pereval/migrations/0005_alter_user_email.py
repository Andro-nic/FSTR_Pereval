# Generated by Django 5.1.2 on 2025-03-05 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_pereval', '0004_levels_remove_pereval_level_autumn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Электронная почта'),
        ),
    ]
