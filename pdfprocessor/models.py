# from django.db import models

from djongo import models


class DocumentAnalysis(models.Model):
    email = models.EmailField(unique=True)
    content = models.TextField()
    nouns = models.TextField()
    verbs = models.TextField()
