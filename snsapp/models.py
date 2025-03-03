from django.db import models

# Create your models here.

class SnsModel(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    author = models.CharField(max_length=20)
    snsimage = models.ImageField(upload_to='')
    good = models.IntegerField(null=True,blank=True,default=0)
    read = models.IntegerField(null=True,blank=True,default=0)
    readtext = models.TextField(null=True,blank=True,default='')