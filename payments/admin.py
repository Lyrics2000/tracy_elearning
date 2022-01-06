from django.contrib import admin

# Register your models here.
from .models import (
    MpesaResquest,
    MpesaQuery
)

admin.site.register(MpesaResquest)
admin.site.register(MpesaQuery)
