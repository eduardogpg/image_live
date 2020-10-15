from django.db import models
from django.conf import settings

from django.db.models.signals import pre_delete

from AWS import upload_file
from AWS import rename_file
from AWS import delete_mediafile

from albums.models import Album

class ImageManager(models.Manager):
    
    def create_by_aws(self, bucket, file, album):
        
        image_key = Image.generate_key(file._name, album)
        
        response = upload_file(bucket, image_key, file)
        if response:
            return self.create(
                key=response._key,
                album=album,
                bucket=response._bucket_name,
                name=file._name,
                size=file.size,
                content_type=file.content_type,
            )

    def delete_by_id(self, id):
        image = self.filter(id=id).first()
        
        if image and image.delete():
            return id

class Image(models.Model):
    key = models.CharField(max_length=50, null=False, blank=False)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=None)
    content_type = models.CharField(max_length=10, null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImageManager()

    def __str__(self):
        return self.key
    
    @classmethod
    def sanitaize_name(cls, name):
        return name.lower().replace(' ', '_')

    @classmethod
    def generate_key(cls, name, album):
        return f'{album.key}{Image.sanitaize_name(name)}'
    
    @property
    def url(self):
        return f'https://{self.bucket}.s3.amazonaws.com/{self.key}'

    @property
    def title(self):
        return self.name.split('.')[0]

    @property
    def extension(self):
        return self.content_type.split('/')[-1]

    def update_name(self, new_name):
        new_image_key = Image.generate_key(new_name, self.album)
        
        if rename_file(self.bucket, new_image_key, self.key):
            self.name = new_name
            self.key = new_image_key
            self.save()

            return self.key

def delete_mediafile_object(sender, instance, using, *args, **kwargs):
    if delete_mediafile(instance.bucket, instance.key) is None:
        raise Exception('Do not delete')

pre_delete.connect(delete_mediafile_object, sender=Image)