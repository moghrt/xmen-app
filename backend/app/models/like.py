from django.db import models
from .post import Post
from django.conf import settings

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'ID: {self.id}, User: { self.user.id }, { self.user.name } Post : { self.post.id }, { self.post.title }'
