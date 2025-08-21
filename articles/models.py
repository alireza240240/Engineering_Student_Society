from django.db import models
from django.conf import settings


class Article(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('approved','approved'),
        ('rejected','Rejected'),
        )
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='pending')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


   