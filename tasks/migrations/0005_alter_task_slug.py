# Generated by Django 4.0.4 on 2022-05-12 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
