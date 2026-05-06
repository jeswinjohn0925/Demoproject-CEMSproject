from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    max_participants = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chest_number = models.CharField(max_length=10, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    @property
    def days_until_event(self):
        delta = self.event.date - timezone.now()
        return max(0, delta.days)

    @property
    def reminder_text(self):
        if self.event.date.date() == timezone.now().date():
            return 'Your event is today. Please arrive early and bring your chest number.'
        days = self.days_until_event
        if days == 1:
            return 'Reminder: Your event is tomorrow. Keep your chest number ready.'
        chest_label = self.chest_number if self.chest_number else 'not assigned yet'
        return f'Upcoming event in {days} days. Your chest number is {chest_label}.'
