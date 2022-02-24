from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
def LoginView(request):
    context = {}

    return render(request,'frontend/login.html',context)

def RegisterView(request):
    context = {}

    return render(request,'frontend/register.html',context)

def ActivateView(request,uidb64,token):
    context = {'uidb64':uidb64,'token':token}

    return render(request,'frontend/activate.html',context)

def ResetView(request):
    context = {}

    return render(request,'frontend/reset.html',context)

def PassewordResetView(request,uidb64,token):
    context = {'uidb64':uidb64,'token':token}

    return render(request,'frontend/passwordreset.html',context)