# Generated by Django 4.0.5 on 2023-02-10 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_remove_checklist_is_done_checklisttype_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='check_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.checklist'),
        ),
    ]