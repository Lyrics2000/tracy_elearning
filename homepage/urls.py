

from django.urls import path
from .views import index,mainpage

app_name = "homepage"

urlpatterns = [
    path('', index,name="homepage"),
    path('dashbord',mainpage,name='dashboard')
]



