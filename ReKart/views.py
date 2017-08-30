from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
#views.py

from django.contrib.auth import logout

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth

from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone

from django.http import Http404
from ReKart.forms import *
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import credentials


def homepage(request):
    args = {}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
        return HttpResponseRedirect("/display/")
    else:
        clear(request)
        return render_to_response(
        'homepage/index.html',
        )
def base(request):
    return render(request,'basic.html')
def contact_us(request):
    args={}
    if 'authenticated' in request.session.keys():
        args['user']=request.session['user']
        args['authenticated']=request.session['authenticated']
    return render(request,'contact.html',args)

def register(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'rekart.django@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/register/success/')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))


def register_success(request):
    args={}
    #args['image']=image
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    return render(request,'registration/success.html',args)
def login1(request):
    if request.method !='POST':
        return render(request, 'registration/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                m = User.objects.get(username=request.POST['username'])
                request.session['user']=request.POST['username']
                request.session['member_id']= m.id
                request.session['authenticated']=True
                print m.id, request.POST['username']
                return HttpResponseRedirect("/display/")
            else:
                message="Please Verify your Account First."
                args = {'message': message}
                return render(request, 'registration/login.html', args)
        else:
            message='SORRY, Wrong Credentials !!!'
            args= {'message': message}
            return render(request, 'registration/login.html',args)

        #print 'In Login1'
        # m = User.objects.get(username=request.POST['username'])
        # if m.password == request.POST['password']:
        #     request.session['member_id']= m.id
        #     print 'In Login2'
        #     return HttpResponseRedirect("display/")

def clear(request):
    params = request.session.keys()
    for param in params:
        del request.session[param]
    return True

def logout(request):
    try:
        '''
        del request.session['user']
        del request.session['member_id']
        '''
        params = request.session.keys()
        for param in params:
            del request.session[param]
    except KeyError:
        pass
    return HttpResponseRedirect('/')




def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/display/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('registration/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('registration/confirm.html')


def upload(request):
    if request.method == 'POST':
        args={}
        args['user']=request.session['user']
        args['authenticated']=request.session['authenticated']
        form = request.POST
        iname=form.get('iname')
        catid=form.get('icat')
        price=form.get('price')
        desc = form.get('desc')
        stateid = form.get('state')
        cityid = form.get('city')
        pin = form.get('pin')
        retdays = form.get('retdays')
        itage =form.get('itage')
        image = request.FILES['img']
        print image
        cat=category.objects.get(id=catid)
        state=states.objects.get(sid=stateid)
        city=cities.objects.get(cid=cityid)
        #mid=User.objects.get(id=5)
        mid=User.objects.get(id=request.session['member_id'])
        Q=item_details(userid=mid,catid =cat,itemname = iname, itemprice = price,
                       description =desc,returndays = retdays,itemage=itage,
                       pin=pin,state=state,city=city,image=image)
        Q.save()
        return render(request, 'uploaded.html',args)
    else:
        #image=UploadImage
        categories=category.objects.all()
        pstates = states.objects.all()
        pcities = cities.objects.all()
        args={}
        #args['image']=image
        args['user']=request.session['user']
        args['authenticated']=request.session['authenticated']
        args['categories']=categories
        args['states']=pstates
        args['cities']=pcities
        args.update(csrf(request))
    return render(request, 'upload.html', args)
def uploaded(request):
    return render(request, 'uploaded.html')
def display(request):
    datas=item_details.objects.all()
    data=[]
    prev=0
    for i in range(4,len(datas),4):
        data.append(datas[prev:i])
        prev=i
    if prev<len(datas):
        data.append(datas[prev:])
    total=len(data)
    args={}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    args['data']=data
    args['total']=total
    return render(request,'display.html',args)

def view(request,itemid):
    item=item_details.objects.get(itemid=int(itemid))
    args = {}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    args['item']=item
    return render(request, 'view.html', args)


#---------------------------------trial add to kart---------------------------------------------
def add_to_kart(request,itemid1):
    if 'authenticated' in request.session.keys():
        mid=User.objects.get(id=request.session['member_id'])
        ids=kart.objects.filter(userid2=mid)
        #print ids
        data=[]
        for id in ids:
            a=item_details.objects.get(itemid=id.itemid2.itemid)
            #print a
            data.append(a)
        #print data
        inp=item_details.objects.get(itemid=itemid1)
        if inp not in data:
            Q=kart(userid2=mid,itemid2=inp)
            Q.save()
        return HttpResponseRedirect('/kart/')
    else:
        return render(request, 'registration/login.html')

def disp_kart(request):
    mid=User.objects.get(id=request.session['member_id'])
    ids=kart.objects.filter(userid2=mid)
    amount=0
    #print ids
    data=[]
    for id in ids:
        a=item_details.objects.get(itemid=id.itemid2.itemid)
        amount+=a.itemprice
        data.append(a)
    total=len(data)
    args={}
    args['amount']=amount
    args['user']=request.session['user']
    args['authenticated']=request.session['authenticated']
    args['data']=data
    args['total']=total
    return render(request,'show_kart.html',args)

def del_from_kart(request,itemid1):
    mid=User.objects.get(id=request.session['member_id'])
    inp=item_details.objects.get(itemid=itemid1)
    Q = kart.objects.get(userid2=mid,itemid2=inp)
    Q.delete()
    return HttpResponseRedirect('/kart/')


#-----------------------------------------------------------------------------------------------
######         PAYPAL       ######

from paypal.standard.forms import PayPalPaymentsForm
@csrf_exempt
def cancel(request):
    args = {}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    return render(request, 'cancel.html',args)
@csrf_exempt
def returnfrompaypal(request):
    args = {}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    return render(request, 'returnfrompaypal.html',args)

def view_that_asks_for_money(request,amount,itemid):
    args={}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
        BASE_URL=credentials.BASE_URL
        Email=credentials.Email
        # What you want the button to do.
        paypal_dict = {
            "business": Email,
            "amount": amount,
            "item_name": "",
            "invoice": "",
            "notify_url": BASE_URL + reverse('paypal-ipn'),
            "return_url": BASE_URL+"/returnfrompaypal/",
            "cancel_return": BASE_URL+"/cancel/",
            "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
        }
        print('itemid= ',itemid)
        a=item_details.objects.get(itemid=int(itemid))
        a.delete()
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        args['form']= form
        args.update(csrf(request))
        return render(request, "payment1.html",args)
    else:
        return render(request, 'registration/login.html')
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != credentials.Email:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            print 'Upgrade Users'
            #Users.objects.update(paid=True)
    else:
        print 'Else Part in show_me_the_money'

valid_ipn_received.connect(show_me_the_money)



###     PAYPAL PRO     ###

from paypal.pro.views import PayPalPro

def nvp_handler(nvp):
    # This is passed a PayPalNVP object when payment succeeds.
    # This should do something useful!
    pass

def buy_my_item(request,amt):
    amt=int(amt)
    args = {}
    args.update(csrf(request))
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
        BASE_URL = 'http://7b78fa35.ngrok.io'
        item = {"amt": amt,  # amount to charge for item
                "inv": "inventory",         # unique tracking variable paypal
                "custom": "tracking",       # custom tracking variable for you
                "cancelurl": BASE_URL+"/cancel/",  # Express checkout cancel url
                "returnurl": BASE_URL+"/returnfrompaypal/"}  # Express checkout return url

        ppp = PayPalPro(
                  item=item,                            # what you're selling
                  payment_template="payment.html",      # template name for payment
                  confirm_template="confirmation.html", # template name for confirmation
                  success_url="/success/",              # redirect location after success
                  nvp_handler=nvp_handler)
        return ppp(request)
    else:
        return render(request, 'registration/login.html')

def success(request):
    args = {}
    if 'authenticated' in request.session.keys():
        args['user'] = request.session['user']
        args['authenticated'] = request.session['authenticated']
    return render(request, 'success.html',args)