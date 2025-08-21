from django.db import models
from django.conf import settings

from news.models import News
from articles.models import Article
from events.models import Event


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    article = models.ForeignKey(Article , on_delete=models.CASCADE , null= True , blank= True , related_name='comments')
    event = models.ForeignKey(Event , on_delete=models.CASCADE , null= True , blank= True , related_name='comments')
    news = models.ForeignKey(News , on_delete=models.CASCADE , null= True , blank= True , related_name='comments')

    def __str__(self):
        return f"Comment by {self.author} - {self.content[:30]}"