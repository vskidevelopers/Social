# Generated by Django 3.1.7 on 2021-11-30 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, unique=True),
        ),
    ]
