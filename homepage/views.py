from django.shortcuts import redirect, render
from account.models import User
from django.forms.models import model_to_dict
from .models import (ScrollingIMages,
AboutUs)
from courses.models import (Courses,Enrolment,
Classes,
Lessons,
LessonFiles,
LessonAssignmentFiles
)
from django.views.generic import DetailView,View,ListView

# Create your views here.

def index(request):
    images =  ScrollingIMages.objects.all()
    about =  AboutUs.objects.all()
    all_courses = Courses.objects.all()
    all_enrolment =  Enrolment.objects.all()


    context ={
        'image' :  images,
        'about' : about,
        'all_courses' :  all_courses
    }
    return render(request,'index.html',context)

def mainpage(request):
    return render(request,'mainpage.html',{})


def about(request):
    all_teachers =  User.objects.all()
    context = {
        'all_teachers' : all_teachers
    }
    return render(request,'about_us.html',context)


def courses(request):


    if request.user.is_authenticated:
        user =  request.user.id
        # get user with the id
        obj = User.objects.get(id=user)
        dict_user =  model_to_dict(obj)
        user_type = dict_user['type']
        courses =  Courses.objects.all()
        all_users =  User.objects.all()
        all_enrolment =  Enrolment.objects.all()
        all_classes =  Classes.objects.all()

        context = {
            'user_type' : user_type,
            'courses' :  courses,
            'all_users' :  all_users,
            'all_enrollmet' :  all_enrolment,
            'all_classes' :  all_classes
            
        }

        return render(request,'courses.html',context)

    
    else:
        courses =  Courses.objects.all()
        all_classes =  Classes.objects.all()

        context = {
            
            'courses' :  courses,
            'all_classes' :  all_classes
            
        }

        return render(request,'courses.html',context)

    
        
        return render(request,'courses.html')


def lesson(request):
    return render(request,'single_lesson.html')


def single_course(request):
    return render(request,'single_course.html')


def get_involved(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        get_course =  Courses.objects.get(id=course_id)
        user_id = request.user.id
        get_user  =  User.objects.get(id=user_id)
        obj,created =  Enrolment.objects.get_or_create(courses_id = get_course,user_id=get_user)
        obj.enrolled =  True
        obj.save()


        return redirect("homepage:courses")



def get_uninvolved(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        get_course =  Courses.objects.get(id=course_id)
        user_id = request.user.id
        get_user  =  User.objects.get(id=user_id)
        obj=  Enrolment.objects.get(courses_id = get_course,user_id=get_user)
        obj.delete()
      


        return redirect("homepage:courses")


class CourseDetailView(DetailView):
    model = Courses
    template_name = "single_course.html"
    def get_context_data(self, **kwargs):
       
        all_enrolment =  Enrolment.objects.all()
        all_lessons =  Lessons.objects.all()

        context = super().get_context_data(**kwargs)
        context['all_enrollement'] = all_enrolment
        context['all_lessons'] =  all_lessons
        
        
        return context


class LessonDetailView(DetailView):
    model = Lessons
    template_name = "single_lesson.html"

    def get_context_data(self, **kwargs):
        all_lessons = Lessons.objects.all()
        all_lesson_files = LessonFiles.objects.all()
        assigments =  LessonAssignmentFiles.objects.all()
        context = super().get_context_data(**kwargs)
        context['all_lessons'] =  all_lessons
        context['lesson_files'] =  all_lesson_files
        context['assignemt_files'] =  assigments

       
        
        
        return context


