from django.db import models

# Create your models here.
class Assessment(models.Model):
    date = models.DateTimeField(auto_now=True)

class File(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    name = models.CharField()

class Error(models.Model):
    File = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    line = models.IntegerField()
    priority = models.IntegerField()
    category = models.CharField()
    text = models.TextField()