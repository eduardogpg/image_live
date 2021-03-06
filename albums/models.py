from django.db import models
from django.db.models import Sum

from AWS import create_folder
from django.contrib.auth.models import User

class AlbumManager(models.Manager):
    
    def create_by_aws(self, bucket, title, description):
        title_sanitaized = title.lower().replace(' ', '_')
        key = create_folder(bucket, title_sanitaized)

        if key:
            return Album.objects.create(title=title, key=key, bucket=bucket, description=description)
        
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
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'key': self.key,
            'bucket': self.bucket
        }
    
    @property
    def images(self):
        return self.image_set.all()

    @property
    def name(self):
        return self.key.replace('/', '')

    @property
    def size(self):
        if self.images:
            return self.images.aggregate(Sum('size'))['size__sum']
        else:
            return 0