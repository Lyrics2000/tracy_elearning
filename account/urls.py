

from django.urls import path
from .views import index,signup

app_name = "account"

urlpatterns = [
    path('', index,name="sign_in"),
    path('signup/', signup,name="sign_up"),
]



