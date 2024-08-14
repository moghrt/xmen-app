from django.db import models
from .user import User
from .room import Room
from django.utils import timesince

class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def __str__(self) -> str:
        return f'Room: {self.room.name} Id: {self.id}, {self.sent_by} : {self.body}'
