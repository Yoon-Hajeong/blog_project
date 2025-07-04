from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Post(models.Model):
    # new_field = models.IntegerField(default=0)
    CATEGORY_CHOICES = [
        ('diary', '영어일기'),
        ('speaking', '영어회화'),
        ('personal_feedback', '학습점검'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='diary'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title