# Generated by Django 3.1.2 on 2020-10-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_remove_image_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
