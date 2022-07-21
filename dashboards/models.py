from statistics import mode
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.
class UserLogs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(default=timezone.now)
    time_out = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'user logs'
    def __Str__(self):
        return self.time_in, self.time_out

class TopDesigner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username()

@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    print(sender)
    print(f'User: {user.username} Logged in' )
    print(user_logged_in)
    if user_logged_in:
        print("User login ")
        user.time_in = timezone.now()
        user.save()

@receiver(pre_save, sender=User)
def pre_save_time_log(sender, instance, *args, **kwargs):
    if user_logged_in:
         print("User login sample")