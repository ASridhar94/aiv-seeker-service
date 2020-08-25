from datetime import datetime

import django
from django.db import models
from django.db.models import CharField, EmailField, DateTimeField, ManyToManyField


class Workflow(models.Model):
    status = CharField(max_length=20, choices=(
        ("SCHEDULED", "SCHEDULED"), ("RUNNING", "RUNNING"), ("SUCCESSFUL", "SUCCESSFUL"), ("FAILED", "FAILED")),
                       default="SCHEDULED")
    submitted_by = CharField(max_length=20, default="guest")  # TODO replace with FK to user.
    email = EmailField()
    submitted_time = DateTimeField(default=django.utils.timezone.now)
    description = CharField(max_length=200, null=True)
    task_id = CharField(max_length=100, null=True)


class SequenceFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
