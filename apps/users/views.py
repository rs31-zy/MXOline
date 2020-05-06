from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from apps.users.form import LoginForm
from django.contrib.auth import authenticate, login
from django.urls import reverse

# Create your views here.
class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'login.html')
    def post(self,request,*args,**kwargs):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username = user_name,password = password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html",{"msg":"用户名密码错误","login_form":login_form})
        else:
            return render(request, "login.html",{"login_form":login_form})

