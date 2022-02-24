from fcntl import F_SEAL_SHRINK
import imp
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Extendeduser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    counter  = models.IntegerField(default=0,null=False)

    def __str__(self):
        return self.user.username

class Loginhistory(models.Model):

    user = models.ForeignKey(User,on_delete = models.CASCADE)
    datetime  = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user.username}_{str(self.datetime.date())}_ {str(self.is_success)}"