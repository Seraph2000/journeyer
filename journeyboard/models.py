from django.db import models

# Create your models here.
class Journey(models.Model):
    # define db schema
    query_from = models.CharField(max_length=100)
    query_to = models.CharField(max_length=100)
    icscode_from = models.CharField(max_length=100)
    icscode_to = models.CharField(max_length=100)
    commonname_from = models.CharField(max_length=100)
    commonname_to = models.CharField(max_length=100)


    def __str__(self):
        # for the admin area
        return '%s %s %s %s %s %s' % (self.query_from, self.query_to, self.icscode_from, self.icscode_to, self.commonname_from, self.commonname_to)