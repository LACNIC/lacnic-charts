from django.db import models

# Create your models here.

import json
import datetime


# class ListField(models.TextField):
#     list = models.CharField(max_length=200)
#
#     def setList(self, x):
#         self.list = json.dumps(x)
#
#     def getList(self, x):
#         return json.loads(self.list)


class CommaSepField(models.Field):
    "Implements comma-separated storage of lists"

    def __init__(self, separator=",", *args, **kwargs):
        self.separator = separator
        super(CommaSepField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CommaSepField, self).deconstruct()
        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

class Chart(models.Model):
    """
        Chart representation
    """
    import django.utils.timezone as tz

    x = models.TextField(default="")
    y = models.TextField(default="")
    xTitle = models.TextField(default="")
    yTitle = models.TextField(default="")
    link = models.TextField(default="")
    dateCreated = models.DateField(default=tz.now())

class EventType():
    CREATE=1
    UPDATE=2
    DELETE=3

class Events(models.Model):
    date = models.DateField()
    type = EventType

