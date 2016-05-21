from django.db import models


class Project(models.Model):

    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)

    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
