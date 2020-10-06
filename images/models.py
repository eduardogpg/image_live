from django.db import models

from AWS.images import upload_image

from django.conf import settings

class ImageManager(models.Manager):

    def create_by_aws(self, local_path, file):
        
        response = upload_image(settings.BUCKET, local_path,
                                    file.content_type, file._name)
        if response:
            return self.create(
                key=response._key,
                bucket=response._bucket_name,
                name=file._name,
                size=file.size,
                content_type=file.content_type,
                extension=Image.get_extension(file._name)
            )

class Image(models.Model):
    key = models.CharField(max_length=50, null=False, blank=False)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    content_type = models.CharField(max_length=10, null=False, blank=False, default='')
    extension = models.CharField(max_length=3, null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImageManager()

    def __str__(self):
        return self.key
    
    @classmethod
    def get_extension(cls, file_name):
        return file_name.split('.')[-1]