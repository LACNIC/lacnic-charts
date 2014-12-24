from django.db import models

# Create your models here.


class Chart(models.Model):
    """
        Chart representation
    """
    data = models.TextField()
    dateCreated = models.DateField()

class EventType():
    CREATE=1
    UPDATE=2
    DELETE=3

class Events(models.Model):
    date = models.DateField()
    type = EventType

