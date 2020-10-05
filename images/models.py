from django.db import models

class Image(models.Model):
    clave = models.CharField(max_length=50, null=False, blank=False)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    content_type = models.CharField(max_length=10, null=False, blank=False, default='')
    extension = models.CharField(max_length=3, null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.clave
    