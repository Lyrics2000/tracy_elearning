from django.db import models
from django.db.models.base import Model
from django.utils.translation import activate
from account.models import User
from django.utils.timezone import now
import random
import os
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from config.utils import unique_slug_generator,category_unique_slug_generator




def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance,filename):
    new_filename = random.randint(1,999992345677653234)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext = ext)
    return "thumbnails/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename = final_filename )



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.

class Classes(BaseModel):
    class_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255,unique=True,blank=True,null=True)

    def get_absolute_url(self):
        return reverse("homepage:course_class_filter", kwargs={
            'slug': self.slug
        })


    def __str__(self):
        return self.class_name


class ClassCategory(BaseModel):
    class_id = models.ForeignKey(Classes,on_delete=models.CASCADE)
    class_title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.class_title

    

def product_presave_reciver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_presave_reciver,sender = ClassCategory)



class Courses(BaseModel):
    title =  models.CharField(max_length=255)
    teacher_id = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    course_category = models.ForeignKey(ClassCategory,on_delete=models.CASCADE)
    short_description = models.TextField(blank=False, max_length=60)
    description = models.TextField(blank=False)
    language = models.CharField(max_length=200) 
    thumbnail = models.ImageField(upload_to='thumbnails/') 
    video_url = models.URLField()
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(blank=True,unique=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("homepage:single_course", kwargs={
            'slug': self.slug
        })

def product_presave_reciver(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_presave_reciver,sender = Courses)


class Enrolment(BaseModel):
    courses_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    enrolled = models.BooleanField(default=False)


    def __str__(self):
        return str(self.courses_id)


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    duration = models.FloatField(validators=[MinValueValidator(0.30), MaxValueValidator(30.00)])
    lesson_body =  models.TextField(blank=True,null=True)
    video_url = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,unique=True,null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("homepage:single_lesson", kwargs={
            'slug': self.slug
        })


class LessonFiles(BaseModel):
    lesson = models.ForeignKey(Lessons,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_description = models.TextField()
    zip_file_upload = models.FileField(upload_to='file_upoaded/')

    def __str__(self):
        return self.file_name


class LessonAssignmentFiles(BaseModel):
    lesson = models.ForeignKey(Lessons,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_description = models.TextField()
    zip_file_upload = models.FileField(upload_to='assignment_upoaded/')

    def __str__(self):
        return self.file_name







