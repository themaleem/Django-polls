from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm

# Create your views here.
def loginview(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            redirect_url=request.GET.get('next','home')
            return redirect(redirect_url)
        else:
            messages.error(request,"Bad username or password")
    context={

    }
    return render(request,'accounts/login.html',context)

def logoutview(request):
    logout(request)
    return redirect('accounts:login')

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid(): 
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            messages.success(request,"Thanks for registering. You can login below")
            return redirect('accounts:login')
    else:
        form=RegistrationForm()
    
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)