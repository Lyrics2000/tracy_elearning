from django.urls import path

from .views import (

    lipa_na_mpesa_online,

    mpesa_queyr,
    startmpesaRequest,
    
)

app_name = "mpesa"
urlpatterns = [
 
    path('online/lipa', lipa_na_mpesa_online, name='lipa_na_mpesa'),

    path('mpesa_query/',mpesa_queyr,name="mpesa_qury"),
    path('startMpesaRequest',startmpesaRequest,name="start_mpesa"),
    

]

