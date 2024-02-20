from django.db import models
from datetime import date, datetime
from django.utils import timezone


class User(models.Model):
    userID = models.CharField(max_length=30)
    timestamp_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
    		return "%s (%s)" % (self.userID, self.timestamp_added)
