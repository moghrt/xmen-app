from django.db import models
from .post import Post
from django.conf import settings

class Comment(models.Model):
    text = models.CharField(max_length=50, default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Id: {self.id},Post { self.post.title }, Comment: {self.text}, Post { self.post.title }, User: { self.user.email }'
