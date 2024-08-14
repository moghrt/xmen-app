from django.db import models
from django.conf import settings

class Room(models.Model):
    GROUPS = 'grupos'
    DIRECT_MESSAGES = 'mensajes'

    TYPES = (
        (GROUPS, 'Grupos'),
        (DIRECT_MESSAGES, 'Mensajes'),
    )

    uuid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, default='')
    tags = models.CharField(max_length=255, blank=True, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='rooms', blank=True, null=True)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    type = models.CharField(max_length=255, choices=TYPES, default=DIRECT_MESSAGES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
   
    def __str__(self):
        return f'{self.name} - {self.caption}'