from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid


@python_2_unicode_compatible
class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_scraped = models.DateTimeField(default=datetime.now)
    date_posted = models.DateTimeField()
    query = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.TextField()
    sponsored = models.BooleanField(default="False")
    expired = models.BooleanField(default="False")
    snippet = models.TextField(default="no description available")
    score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return 'company: ' + self.company + ', title: ' + self.title + ', posted: ' + \
        self.date_posted.strftime("%B %d, %Y") + ', query: ' + query