from django.db import models
from project import project_types


class Lab(models.Model):
    name = models.CharField(max_length=16)
    project_type = models.CharField(max_length=32,
            choices=project_types, default="Other")

    def __unicode__(self):
        return self.name
