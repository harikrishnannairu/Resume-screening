from django.db import models

# Create your models here.


class Resumes(models.Model):
    resume_id = models.IntegerField(primary_key=True)
    candidate_name = models.CharField(max_length=60)
    file = models.FileField()

class Screen(models.Model):
    rank_id=models.IntegerField(primary_key=True)
    candidate_name=models.CharField(max_length=60)
    file= models.FileField()
    resume_score=models.FloatField()