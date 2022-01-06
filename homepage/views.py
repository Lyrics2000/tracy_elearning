from django.core.validators import slug_re
from django.shortcuts import redirect, render
from account.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
import uuid
from sklearn.neighbors import NearestNeighbors
from django.http import Http404

from .models import (ScrollingIMages,
AboutUs)
from account.models import Profile_pic
from courses.models import (ClassCategory, Courses,Enrolment,
Classes,
Lessons,
LessonFiles,
LessonAssignmentFiles,
Ratting
)
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,View,ListView

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from account.models import ChildEmail


# machine learning recommendation
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_obj =  User.objects.get(id= user_id)
        images =  ScrollingIMages.objects.all()
        about =  AboutUs.objects.all()
        all_courses = Courses.objects.all()
        all_enrolment =  Enrolment.objects.filter(user_id = user_obj)
        print(all_enrolment)
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
        all_enrolment =  Enrolment.objects.filter(user_id = obj)
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            file_name =  request.POST.get('file_name')
            file_description =  request.POST.get('file_description')
            file = request.FILES['file']
            lesson_id =  request.session['class_lesson_id']
            course_obj =  Lessons.objects.get(id =  lesson_id)
            slug =  str(uuid.uuid4().hex) + str(file_name).strip().replace(" ","_")
            LessonFiles.objects.create(lesson = course_obj,
            file_name = file_name,
            file_description =  file_description,
            zip_file_upload = file
            )
            return redirect("homepage:upload_assingment_file")

    return render(request,'upload_lesson_file.html')


def upload_assingment_file(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user =  request.user
            file_name =  request.POST.get('file_name')
            file_description =  request.POST.get('file_description')
            file = request.FILES['file']
            lesson_id =  request.session['class_lesson_id']
            course_obj =  Lessons.objects.get(id =  lesson_id)
            slug =  str(uuid.uuid4().hex) + str(file_name).strip().replace(" ","_")
            LessonAssignmentFiles.objects.create(lesson = course_obj,
            file_name = file_name,
            file_description =  file_description,
            zip_file_upload = file
            )
            current_site = get_current_site(request)
            email_subject = 'Successfull Uploaded'
            message = render_to_string('successfull_uploaded.html', {
            'user': user,
            'domain': current_site.domain
            })
            to_email = user.email
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return redirect("/")
    return render(request,'upload_lesson_assignment.html')



def student_enrolled_parent(request):
    user_id =  request.user.id
    user_obj =  User.objects.get(id =  user_id)
    child =  ChildEmail.objects.get(parent_id =  user_obj)
    child_email = child.child_email

    user_child =  User.objects.get(email =child_email)
    enrolled_child = Enrolment.objects.filter(user_id =  user_child)
    print(enrolled_child)


    context = {
        'enrolled':  enrolled_child
    }


    return render(request,'student_enrolled_class.html',context)






def courses_recommeondations(request):
    user_id =  request.user.id
    user_obj  = User.objects.all()
    courses =  Courses.objects.all()
    df = pd.DataFrame(np.zeros(shape=(len(user_obj),len(courses))))
    print(str(df))
    col_names = []
    row_names = []
    for u  in courses:
        col_names.append(u.id)
    print(col_names)

    for lk in user_obj:
        row_names.append(lk.id)
    print(row_names)

    df.columns = col_names
    df.index = row_names

    print(df)
   
   
    for m in user_obj:
        for l in courses:
            course_obj =  Courses.objects.get(id =  l.id)
            user_obj =  User.objects.get(id =  m.id)
            try:
                rete =  Ratting.objects.get(courses_id_id =  l.id,user_id_id =  m.id)
                print("mkk",df.at[m.id,l.id])
                df.at[m.id,l.id] = rete.ratting
                print(rete.ratting)
                
            except Ratting.DoesNotExist:
                pass

    
    print(df)
    # calculating nearest neighbors
    # transposing the dataframe
    df1 = df.T
    df2 = df.T
    
    # find the nearest neighbors using NearestNeighbors(n_neighbors=3)
    number_neighbors = 3
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df1.values)
    distances, indices = knn.kneighbors(df1.values, n_neighbors=number_neighbors)
    # convert user_name to user_index
    user_index = df1.columns.tolist().index(request.user.id)
    print(user_index)

    # t: courses_title, m: the row number of t in df1
    for m,t in list(enumerate(df1.index)):
        # find course without ratings by user
        

        if df1.iloc[m, user_index] == 0:
            sim_course = indices[m].tolist()
            course_distances = distances[m].tolist()

        # Generally, this is the case: indices[3] = [3 6 7]. The course itself is in the first place.
        # In this case, we take off 3 from the list. Then, indices[3] == [6 7] to have the nearest NEIGHBORS in the list. 
        if m in sim_course:
            id_course = sim_course.index(m)
            sim_course.remove(m)
            course_distances.pop(id_course)
        # However, if the percentage of ratings in the dataset is very low, there are too many 0s in the dataset. 
        # Some courses have all 0 ratings and the courses with all 0s are considered the same courses by NearestNeighbors(). 
        # Then,even the course itself cannot be included in the indices. 
        # For example, indices[3] = [2 4 7] is possible if course_2, course_3, course_4, and course_7 have all 0s for their ratings.
        # In that case, we take off the farthest course in the list. Therefore, 7 is taken off from the list, then indices[3] == [2 4].
        else:
            sim_course = sim_course[:number_neighbors-1]
            course_distances = course_distances[:number_neighbors-1]


        # course_similarty = 1 - course_distance    
        course_similarity = [1-x for x in course_distances]
        course_similarity_copy = course_similarity.copy()
        nominator = 0

         # for each similar course
        for s in range(0, len(course_similarity)):
            # check if the rating of a similar course is zero
            if df1.iloc[sim_course[s], user_index] == 0:
                # if the rating is zero, ignore the rating and the similarity in calculating the predicted rating
                if len(course_similarity_copy) == (number_neighbors - 1):
                    course_similarity_copy.pop(s)
                else:
                    course_similarity_copy.pop(s-(len(course_similarity)-len(course_similarity_copy)))

            # if the rating is not zero, use the rating and similarity in the calculation
            else:
                nominator = nominator + course_similarity[s]*df.iloc[sim_course[s],user_index]

            # check if the number of the ratings with non-zero is positive
            if len(course_similarity_copy) > 0:
                # check if the sum of the ratings of the similar courses is positive.
                if sum(course_similarity_copy) > 0:
                    predicted_r = nominator/sum(course_similarity_copy)

                # Even if there are some courses for which the ratings are positive, some courses have zero similarity even though they are selected as similar courses.
                # in this case, the predicted rating becomes zero as well  
                else:
                    predicted_r = 0
            # if all the ratings of the similar courses are zero, then predicted rating should be zero
            else:
                predicted_r = 0

            # place the predicted rating into the copy of the original dataset
            df2.iloc[m,user_index] = predicted_r


        def recommend_course(user, num_recommended_courses):
            print('The list of the course {} Has Watched \n'.format(user))

            for m in df1[df1[user] > 0][user].index.tolist():
                print(m)

            print('\n')

            recommended_course = []
            cours_m = []
            for m in df1[df1[user] == 0].index.tolist():

                index_df = df1.index.tolist().index(m)
                predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
                print(",,,",m)
                recommended_course.append((m, predicted_rating))
                

            sorted_rm = sorted(recommended_course, key=lambda x:x[1], reverse=True)
            print('The list of the Recommended course \n')
            rank = 1
            for recommended_course in sorted_rm[:num_recommended_courses]:
                print('{}: {} - predicted rating:{}'.format(rank, recommended_course[0], recommended_course[1]))
                rank = rank + 1

            return sorted_rm

        
        recs = recommend_course(request.user.id, len(courses))
        print("mksi",recs)
        course_idds = []
        for k in recs:
            cour = Courses.objects.get(id = int(k[0]))
            course_idds.append(cour)

        all_classes =  Classes.objects.all()
        
        context = {
            'courses':course_idds,
            'all_classes':all_classes
        }
        print(course_idds)
         

            
        
    # combine a value of important search names to a string
    
    return render(request,'recommendations.html',context)



@login_required(login_url="account:sign_in")
def rattings(request):
    if request.method  == "POST":
        user_id =  request.user.id
        user_obj =  User.objects.get(id = user_id)
        course_id =  request.POST.get("course_id")
        course_obj =  Courses.objects.get(id =  int(course_id))
        ratting =  request.POST.get("ratting")
        print("ratting : ",ratting)
        obj,created = Ratting.objects.get_or_create(courses_id = course_obj,user_id =  user_obj)
        obj.ratting = ratting
        obj.save()
        return HttpResponseRedirect(f'/single_course/{course_obj.slug}/')

    


