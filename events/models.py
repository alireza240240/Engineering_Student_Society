from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateTimeField() # zmn brgzri
    capacity =  models.PositiveIntegerField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def spots_left(self):
        return self.capacity - self.participants.count()

class EventParticipant(models.Model):
    event = models.ForeignKey(Event,related_name='participants' , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event','user')

    def __str__(self):
        return f"{self.user.username} -->> {self.event.title}"