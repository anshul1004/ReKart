from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone



import datetime,time
from datetime import date
from django.utils import timezone
from time import time

from django.db import models
from django.contrib.auth.models import User

def get_upload_file_name(instance,filename):
    print 'filename is %s' %(filename)
    return "images/%s" % (filename)



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

# Create your models here.



class states(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=128)

class cities(models.Model):
    cid = models.AutoField(primary_key=True)
    sid = models.ForeignKey(states, to_field='sid')
    cname = models.CharField(max_length=128)
class user_details(models.Model):
    userid = models.ForeignKey(User,to_field='id')
    phone = models.IntegerField()
    address = models.CharField(max_length=256)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    pin = models.IntegerField()

class category(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=3,unique=True)
    cname = models.CharField(max_length=64)

class item_details(models.Model):
    itemid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User,to_field='id', default=1)
    catid = models.ForeignKey(category,to_field='cid')
    itemname = models.CharField(max_length=256)
    itemprice = models.IntegerField()
    description = models.TextField(max_length=1024)
    returndays = models.IntegerField(default=0)
    postingdate = models.DateField(default=date.today(),null=False)
    itemage = models.IntegerField()
    pin=models.IntegerField()
    city = models.ForeignKey(cities,to_field='cid')
    state = models.ForeignKey(states,to_field='sid')
    image = models.FileField(upload_to=get_upload_file_name)

class images(models.Model):
    itemid = models.ForeignKey(item_details, to_field='itemid')
    image = models.ImageField(null=True)

#----------------------------------------------trial for kart---------------------------
class kart(models.Model):
    userid2=models.ForeignKey(User,to_field='id')
    itemid2=models.ForeignKey(item_details,to_field='itemid')
#-----------------------------------------------------------------------------------------------