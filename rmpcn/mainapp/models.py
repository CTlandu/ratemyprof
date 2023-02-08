from django.db import models

# Create your models here.
class Instructor(models.Model):
  instructor_name=models.CharField(verbose_name="老师名", max_length=64)
  average_rate=models.IntegerField(verbose_name="评分")
