from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=50, default="Nuevo post")
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Id: {self.id}, User: { self.user.email } Post title: { self.title }, Likes: {self.likes}'
