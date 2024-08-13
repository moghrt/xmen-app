from django.db import models
from django.conf import settings

class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, default='')
    tags = models.CharField(max_length=255, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='rooms', blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
   
    def __str__(self):
        return f'{self.client} - {self.caption}'