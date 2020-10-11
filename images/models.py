from django.db import models
from django.conf import settings

from AWS import upload_file

from albums.models import Album

class ImageManager(models.Manager):
    
    def create_by_aws(self, bucket, file, title, album):
        
        type = file.content_type.split('/')[-1]

        title_sanitaized = title.lower().replace(' ', '_')
        title_sanitaized = f'{title_sanitaized}.{type}'
        
        key = f'{album.key}{title_sanitaized}'
        response = upload_file(bucket, key, file)

        if response:
            return self.create(
                key=response._key,
                album=album,
                bucket=response._bucket_name,
                name=file._name,
                size=file.size,
                content_type=file.content_type,
                extension='png'
            )

class Image(models.Model):
    key = models.CharField(max_length=50, null=False, blank=False)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100)
    size = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=None)
    content_type = models.CharField(max_length=10, null=False, blank=False, default='')
    extension = models.CharField(max_length=3, null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImageManager()

    def __str__(self):
        return self.key
    
    @property
    def url(self):
        return f'https://{self.bucket}.s3.amazonaws.com/{self.key}'