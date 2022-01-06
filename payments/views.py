from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from payments.mpesa.services import PaymentService
import json
from django.template.loader import render_to_string
import time
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .utils import validate_not_mobile
from account.models import User
from courses.models import Lessons
from payments.mpesa.mpesa_credentials import MpesaC2bCredential
from .models import MpesaResquest,MpesaQuery
from django.http import HttpResponseRedirect
 

# Create your views here.
@login_required(login_url="account:sign_in")
def lipa_na_mpesa_online(request):
    if request.method == "POST":
        phone_number  =  request.POST.get('phone')
        lesson_id  =  request.POST.get("lesson_id")
        request.session['phone'] = phone_number
        request.session['lesson_id'] =  lesson_id
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True)
        access_token = lipa_na_mpesa.get_access_token()
        if len(access_token) > 0:
            return redirect ('mpesa:start_mpesa')
        return render(request,'mpesa_erro.html',{})
                



@login_required(login_url="account:sign_in")
def startmpesaRequest(request):

    print("...........beginning mpesa request..................")
    phone_number  =  request.session.get('phone')
    print(phone_number)
    lesson_id =  request.session.get('lesson_id')
    lesson_obj = Lessons.objects.get(id = lesson_id)
    user_id = request.user.id
    user_obj =  User.objects.get(id= user_id)
    
    callbackurl = "https://shrouded-reef-57090.herokuapp.com/payment/c2b/confirmation/"
    lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True) 
    app =  lipa_na_mpesa.process_request(phone_number=validate_not_mobile(str(phone_number)),amount=1,callback_url=callbackurl,reference="Lesson Files Payment",description="payment for lesson files")
    print(app)
    r = json.dumps(app)
    js = json.loads(r)
    if js["status"] == "Started":
        if int(js["response"]['ResponseCode']) == 0:
            obj = MpesaResquest.objects.create(user_id = user_obj,
             lesson_id= lesson_obj,
             merchantRequestid = js["response"]['MerchantRequestID'],
             chechoutrequestid = js["response"]['CheckoutRequestID'] ,
             responsecode = js["response"]['ResponseCode'] ,
             responsedescription =  js["response"]['ResponseDescription'],
             customerMessage = js["response"]['CustomerMessage'],
             status = js["status"],
             request_id = js["request_id"],
             callback_url = callbackurl)
           
            request.session['checkout_id'] = js["response"]['CheckoutRequestID']
            request.session['merchant_id'] = js["response"]['MerchantRequestID']
            request.session['phone_no'] = phone_number
          
            return redirect('mpesa:mpesa_qury')

        else:
            return render(request,'mpesa_erro.html',{})
    else:
        return render(request,'mpesa_erro.html',{})


@login_required(login_url="account:sign_in")
def mpesa_queyr(request):
    checkout_id = request.session.get('checkout_id' ,  None)
    merchant_id =  request.session.get('merchant_id', None)
    phone_no = request.session.get('phone_no', None)

    if((checkout_id is not None) and ( merchant_id is not None) and (phone_no is not None)):
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True)
        time.sleep(20)
        mpesa_request = lipa_na_mpesa.query_request(checkout_id)
        print(mpesa_request,"mpesa request")
        if mpesa_request["status"] == "Success":
            print("running next")
            mpesa_rs = MpesaResquest.objects.get(merchantRequestid = merchant_id, chechoutrequestid = checkout_id )
            objf,created = MpesaQuery.objects.get_or_create(mpesa_request_id = mpesa_rs )
            objf.response_code = mpesa_request['response']['ResponseCode']
            print("1")
            objf.response_description = mpesa_request['response']['ResponseDescription']
            objf.merchant_id = mpesa_request['response']['MerchantRequestID']
            print("2")
            objf.checkout_request_id = mpesa_request['response']['CheckoutRequestID']
            print("3")
            objf.result_code = mpesa_request['response']['ResultCode']
            print("4")
            objf.result_description = mpesa_request['response']['ResultDesc']
            print("5")
            objf.status =  mpesa_request['status']
            print("6")
            objf.request_id =  mpesa_request['request_id']
            objf.save()

            lesson_id = request.session.get('lesson_id')
            lesson_obj =  Lessons.objects.get(id =  lesson_id)
            
            lesson_obj.paid =  True
            lesson_obj.save()
            email_subject = 'Lesson File Payment'
            user =  request.user
            current_site = get_current_site(request)
            message = render_to_string('sucess_lesson.html', {
            'user': user,
            'domain': current_site.domain,
            })
            to_email = user.email
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            
            print("3")
         
            return HttpResponseRedirect('/single_lesson/%d/'%int(lesson_id))

        
        return render(request,'mpesa_erro.html',{})
    return render(request,'mpesa_erro.html',{})
  