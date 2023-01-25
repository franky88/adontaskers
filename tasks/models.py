from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
import uuid
# Create your models here.


class BaseTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.created


class TaskCategory(BaseTime, models.Model):
    name = models.CharField(max_length=120, unique=True)
    task_point = models.FloatField(default=0.0)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Task Categories"

    def __str__(self):
        return self.name


class TaskType(BaseTime, models.Model):
    name = models.CharField(max_length=60)
    task_point = models.FloatField(default=0.0)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='designers')
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, default=1)
    task_category = models.ForeignKey(
        TaskCategory, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=120, verbose_name="Client name")
    paradise_link = models.URLField(
        blank=True, null=True, verbose_name="task link")
    check_list_link = models.URLField(
        max_length=120, verbose_name='check list link', blank=True, null=True)
    # task_note = models.TextField(blank=True, null=True, help_text='Task note for designers')
    is_priority = models.BooleanField(
        default=False, verbose_name="Is Task Priority?", help_text="Checked if task is priority.")
    is_done = models.BooleanField(default=False, verbose_name="Is Task Completed?",
                                  help_text="Note: Checked if you're done.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_priority', 'is_done', '-updated', '-created']

    def get_absolute_url(self):
        return reverse("taskdetail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class TaskRemark(BaseTime, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    remarks = models.TextField(help_text="You can html elements for your notes")

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.task.name


@receiver(post_save, sender=Task)
def pre_save_task_slug(instance, created, *args, **kwargs):
    if created:
        slug = slugify(instance.name + " " +
                       str(uuid.uuid4()).replace("-", "").upper()[:8])
        instance.slug = slug
        instance.save()
