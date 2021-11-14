from django.db import models
import os
import random

# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance,filename):
    new_filename = random.randint(1,999992345677653234)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext = ext)
    return "thumbnails/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename = final_filename )


class ScrollingIMages(models.Model):
    heading =  models.CharField(max_length=255)
    image = models.ImageField(upload_to = upload_image_path)

    def __str__(self):
        return self.heading


class AboutUs(models.Model):
    heading = models.CharField(max_length=255)
    body =  models.TextField()
    image =  models.ImageField(upload_to=upload_image_path)

    def __str__(self):
        return self.heading

