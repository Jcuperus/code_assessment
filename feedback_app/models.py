from django.db import models

# Create your models here.
class Assessment(models.Model):
    date = models.DateTimeField(auto_now=True)

class SourceFile(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Error(models.Model):
    source_file = models.ForeignKey(SourceFile, on_delete=models.CASCADE)
    begin_line = models.IntegerField()
    end_line = models.IntegerField()
    priority = models.IntegerField()
    category = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
