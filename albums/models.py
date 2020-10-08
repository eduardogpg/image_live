from django.db import models

from AWS import create_folder
from django.contrib.auth.models import User

class AlbumManager(models.Manager):
    
    def create_by_aws(self, bucket, title, description):
        
        title_sanitaized = title.lower().replace(' ', '_')
        key = create_folder(bucket, title_sanitaized)
        
        if key:
            return Album.objects.create(title=title, key=key,
                                        bucket=bucket, description=description)
        
class Album(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    key = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AlbumManager()

    def __str__(self):
        return self.title

    @property
    def serializer(self):
        return {
            'id': album.id,
            'title': album.title,
            'description': album.description,
            'key': album.key,
            'bucket': album.bucket
        }