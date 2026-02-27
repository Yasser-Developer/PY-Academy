from django.db import models

class Competition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name