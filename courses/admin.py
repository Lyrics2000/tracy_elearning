from django.contrib import admin
from .models import (Classes,
ClassCategory,Courses,Enrolment,Lessons,
LessonFiles,LessonAssignmentFiles,
Ratting)

# Register your models here.
admin.site.register(Classes)
admin.site.register(Courses)
admin.site.register(ClassCategory)
admin.site.register(Enrolment)
admin.site.register(Lessons)
admin.site.register(LessonFiles)
admin.site.register(LessonAssignmentFiles)
admin.site.register(Ratting)

