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





from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.http import Http404
from ReKart.forms import *
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


#@csrf_protect
# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.create_user(
#             username=form.cleaned_data['username'],
#             password=form.cleaned_data['password1'],
#             email=form.cleaned_data['email']
#             )
#             return HttpResponseRedirect('/register/success/')
#     else:
#         form = RegistrationForm()
#     variables = RequestContext(request, {
#     'form': form
#     })
#
#     return render_to_response(
#     'registration/register.html',
#     variables,
#     )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
def login(request):
    if request.method !='POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = User.objects.get(username=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id']= m.id
            return HttpResponseRedirect("/home/")
    except User.DoesNotExist:
        return HttpResponseRedirect("/accounts/login/")


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')


#def logout_page(request):
 #   logout(request)
  #  return HttpResponseRedirect('/')





