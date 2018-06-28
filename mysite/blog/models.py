from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    TABLE_OF_CHOICES = (('draft','Roboczy'),('published','Opublikowany'),)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    body_text = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length = 20, choices= TABLE_OF_CHOICES, default = 'draft'  )

    def published(self):
        self.publish = timezone.now()
        self.save()

    def __str__(self):
        return self.title
