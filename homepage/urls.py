

from django.urls import path
from .views import (index,
mainpage,
about,
courses,
lesson,get_involved,
get_uninvolved,
CourseDetailView,
LessonDetailView,
courses_class_filter)

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
    path('single_lesson/<slug>/',LessonDetailView.as_view(),name="single_lesson"),
    path('course_class_filter/<slug>/',courses_class_filter,name="course_class_filter")
]



