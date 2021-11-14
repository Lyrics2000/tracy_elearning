

from django.urls import path
from .views import (index,
mainpage,
about,
courses,
lesson,get_involved)

app_name = "homepage"

urlpatterns = [
    path('', index,name="homepage"),
    path('dashbord',mainpage,name='dashboard'),
    path('about/',about,name="about"),
    path('courses/',courses,name="courses"),
    path('single_lesson/',lesson,name="lesson"),
    path('get_involved/',get_involved,name="get_involved")
]



