from datetime import timedelta

from django.db import models

# Create your models here.

class Recipes(models.Model):
    Name=models.CharField(max_length=200)
    Prep_time=models.DurationField(default=timedelta(minutes=120))
    DIFICULTY_CHOICES=[
        (1,'Easy'),
        (2, 'Medium'),
        (3, 'Hard')
    ]
    Difficulty=models.IntegerField(choices=DIFICULTY_CHOICES)
    Vegetarian=models.BooleanField()
    Recip_img=models.ImageField(upload_to='recipes/')
    Descriptions=models.CharField(max_length=5000)
