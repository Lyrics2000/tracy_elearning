from os import SCHED_BATCH
from django.contrib import admin
from .models import (
    ScrollingIMages,
    AboutUs
)

# Register your models here.
admin.site.register(ScrollingIMages)
admin.site.register(AboutUs)
