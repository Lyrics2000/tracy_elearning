from django.shortcuts import redirect, render
from .forms import SignINForm,SignUpForm
from django.contrib.auth import authenticate,login
# from django.contrib.auth.models import User
from account.models import User


# Create your views here.
def index(request):

    login_form = SignINForm(request.POST,None)

    
    context = {
        'login' : login_form
    }
    
    if login_form.is_valid:
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request,username = username, password = password )
        print("jjja",user)
        if user is not None:
        
            login(request,user)
            return redirect("homepage:homepage")
        else:
            pass
    return render(request,'signin.html',context)


def signup(request):
    sign_up = SignUpForm(request.POST,None)

    context =  { 
        "form" :sign_up
    }
    if request.method =='POST':
        if sign_up.is_valid:
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name =  request.POST.get("last_name")
            type = request.POST.get("type")
            phone =  request.POST.get("phone")
            email = request.POST.get('email')
            password = request.POST.get("password")
            user = authenticate(request,username = email, password = password )
            if user is not None:
                print("user exists")
                return redirect("account:sign_in")
            else:
                
                user = User.objects.create_user(username = username , email = email , password = password)
                user.last_name = last_name
                user.first_name = first_name
                user.type =  type
                user.phone = phone
                user.save()

                userr = authenticate(request,username = email, password = password )
                if userr is not None:
                    login(request,userr)
                    return redirect("homepage:homepage")

    return render(request,'signup.html',context)