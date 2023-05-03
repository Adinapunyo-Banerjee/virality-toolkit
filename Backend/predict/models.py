from django.db import models

# Create your models here.

from datetime import datetime

CATEGORY_CHOICES = [
    (1 , 'Gaming'),
    (2 , 'Development'),
    (3 , 'Cars')
]

from django.conf import settings

class predictionModel1(models.Model):
    thumb = models.ImageField(upload_to='prediction_model1')
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    subscribers = models.IntegerField(default=0)
    channel_pub_time = models.DateTimeField(default=datetime.now, blank=True)       # Passing reference to the function!
    video_pub_time = models.DateTimeField(default=datetime.now, blank=True)
    videos = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)