from django.core.validators import slug_re
from django.shortcuts import redirect, render
from account.models import User
from django.forms.models import model_to_dict
import uuid

from .models import (ScrollingIMages,
AboutUs)
from account.models import Profile_pic
from courses.models import (ClassCategory, Courses,Enrolment,
Classes,
Lessons,
LessonFiles,
LessonAssignmentFiles
)
from django.views.generic import DetailView,View,ListView

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_obj =  User.objects.get(id= user_id)
        images =  ScrollingIMages.objects.all()
        about =  AboutUs.objects.all()
        all_courses = Courses.objects.all()
        all_enrolment =  Enrolment.objects.all()
        profile_pic =  Profile_pic.objects.all()

        context ={
            'image' :  images,
            'about' : about,
            'all_courses' :  all_courses,
            'all_enrollmet' : all_enrolment,
            'profile_pic' : profile_pic

        }
        return render(request,'index.html',context)

    else:
        images =  ScrollingIMages.objects.all()
        about =  AboutUs.objects.all()
        all_courses = Courses.objects.all()
        


        context ={
            'image' :  images,
            'about' : about,
            'all_courses' :  all_courses,
            

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
      
        all_users =  User.objects.all()
        all_enrolment =  Enrolment.objects.all()
        all_classes =  Classes.objects.all()
        context = {
            'courses' :  courses,
            'all_classes' :  all_classes
            
        }

        return render(request,'courses.html',context)

    
        
        


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






def single_lesson(request,slug):
    singe_l = Lessons.objects.get(id =  slug)
    all_lessons = Lessons.objects.all()
    all_lesson_files = LessonFiles.objects.all()
    assigments =  LessonAssignmentFiles.objects.all()

    context = {
        'object':singe_l,
        'all_lessons' :  all_lessons,
        'lesson_files' :  all_lesson_files,
        'assignemt_files' :  assigments

    }

    return render(request,'single_lesson.html',context)



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


def courses_class_filter(request, slug):
    if request.user.is_authenticated:
        user =  request.user.id
        # get user with the id
        obj = User.objects.get(id=user)
        dict_user =  model_to_dict(obj)
        user_type = dict_user['type']
        courses =  Courses.objects.all()
        all_users =  User.objects.all()
        all_enrolment =  Enrolment.objects.all()
        print(slug)
        filtered_classes =  Classes.objects.get(id= slug)
        all_classes =  Classes.objects.all()

        context = {
            'user_type' : user_type,
            'courses' :  courses,
            'all_users' :  all_users,
            'all_enrollmet' :  all_enrolment,
            'all_classes' :  all_classes,
            'filtered_classes' :  filtered_classes
            
        }

        return render(request,'classes_filter.html',context)

    
    else:
        courses =  Courses.objects.all()
        all_classes =  Classes.objects.all()
        filtered_classes =  Classes.objects.get(slug= slug)

        context = {
            
            'courses' :  courses,
            'all_classes' :  all_classes,
            'filtered_classes ' :  filtered_classes
            
        }

        return render(request,'classes_filter.html',context)


def upload_class(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            class_name =  request.POST.get('class_name')
            user =  request.user.id
            # get user with the id
            obju = User.objects.get(id=user)
            slug =  str(uuid.uuid4().hex) + str(class_name).strip().replace(" ","_")
            obj,created = Classes.objects.get_or_create(user_id = obju,slug = slug)
            obj.class_name = class_name
            obj.active =  True
            obj.save()
            request.session['class_id'] = obj.id
            return redirect("homepage:class_category_upload")
    return render(request,'upload_class.html')



def upload_class_category(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            class_name =  request.POST.get('class_title')
            class_uploaded =  request.session['class_id']
            get_class =  Classes.objects.get(id= int(class_uploaded))
            slug =  str(uuid.uuid4().hex) + str(class_name).strip().replace(" ","_")
            obj,created = ClassCategory.objects.get_or_create(class_id = get_class,slug=slug)
            obj.class_title = class_name
            obj.save()
            request.session['class_category_id'] = obj.id
            return redirect("homepage:upload_courses")
    return render(request,'upload_class_category.html')


def upload_courses(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            class_name_title = request.POST.get('course_title')
            class_short_description = request.POST.get('course_short_description')
            class_long_description = request.POST.get('course_long_description')
            class_language = request.POST.get('course_language')
            class_thumbnails = request.FILES['course_thumbnail']
            class_video_url = request.POST.get('video_url')
            user_id =  request.user.id
            user_obj =  User.objects.get(id=  user_id)
            class_category =  request.session['class_category_id']
            slug =  str(uuid.uuid4().hex) + str(class_name_title).strip().replace(" ","_")
            class_category_obj = ClassCategory.objects.get(id =  class_category)
            couses =  Courses.objects.create(
                title = class_name_title,
                teacher_id = user_obj,
                course_category = class_category_obj,
                short_description = class_short_description,
                description = class_long_description,
                language = class_language,
                thumbnail = class_thumbnails,
                video_url = class_video_url,
                is_published = True,
                slug = slug
            )
            request.session['class_courses_id'] = couses.id
            return redirect("homepage:upload_lessons")
    
    return render(request,'upload_courses.html')


def lesson_upload_ff(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            lesson_title =  request.POST.get('lesson_title')
            lesson_duration =  request.POST.get('lesson_duration')
            print(lesson_duration)
            lesson_body = request.POST.get('lesson_body')
            video_url =  request.POST.get('video_url')
            course_id =  request.session['class_courses_id']
            course_obj =  Courses.objects.get(id =  course_id)
            slug =  str(uuid.uuid4().hex) + str(lesson_title).strip().replace(" ","_")
            lessons,created =  Lessons.objects.get_or_create(course = course_obj,slug=slug)
            lessons.title =  lesson_title
            lessons.duration =  float(lesson_duration)
            lessons.lesson_body = lesson_body
            lessons.video_url =  video_url
            lessons.save()
            request.session['class_lesson_id'] = lessons.id
            return redirect("homepage:upload_lessons_file")


    return render(request,'upload_lesson.html')



def lesson_file_upload(request):
    return render(request,'upload_lesson_file.html')




    


