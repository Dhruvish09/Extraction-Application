# models.py

from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    file_url = models.URLField(null=True, blank=True)  # This can be used to store file's URL
    created_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.file.name if self.file else self.url}'


class FailedUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
