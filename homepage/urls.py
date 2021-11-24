

from os import name
from django.urls import path
from .views import (index,
mainpage,
about,
courses,
lesson,get_involved,
get_uninvolved,
CourseDetailView,
LessonDetailView,
courses_class_filter,
upload_class,
upload_class_category,
upload_courses,
single_lesson,
lesson_upload_ff,
lesson_file_upload,
upload_assingment_file)

app_name = "homepage"

urlpatterns = [
    path('', index,name="homepage"),
    path('dashbord',mainpage,name='dashboard'),
    path('about/',about,name="about"),
    path('courses/',courses,name="courses"),
    path('single_lesson/',lesson,name="lesson"),
    path('get_involved/',get_involved,name="get_involved"),
    path('get_uninvolved',get_uninvolved,name="get_uninvolved"),
    path('single_course/<slug>/',CourseDetailView.as_view(),name="single_course"),
    path('single_lesson/<slug>/',single_lesson,name="single_lesson"),
    path('course_class_filter/<slug>/',courses_class_filter,name="course_class_filter"),
    path('upload_class/',upload_class,name="upload_class"),
    path("class_category_upload/",upload_class_category, name="class_category_upload"),
    path('upload_courses/',upload_courses,name="upload_courses"),
    path('upload_lesson/',lesson_upload_ff,name="upload_lessons"),
    path('upload_lesson_file/',lesson_file_upload,name="upload_lessons_file"),
    path('upload_assingment_file/',upload_assingment_file,name="upload_assingment_file")

]



