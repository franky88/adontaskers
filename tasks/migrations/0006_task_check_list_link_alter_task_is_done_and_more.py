# Generated by Django 4.0.4 on 2022-06-06 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='check_list_link',
            field=models.URLField(blank=True, max_length=120, null=True, verbose_name='ckeck list link'),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_done',
            field=models.BooleanField(default=False, help_text="Note: Checked if you're done.", verbose_name='Is done?'),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_priority',
            field=models.BooleanField(default=False, help_text='Checked if task is priority.', verbose_name='Is Priority?'),
        ),
        migrations.AlterField(
            model_name='task',
            name='paradise_link',
            field=models.URLField(blank=True, null=True, verbose_name='task link'),
        ),
    ]