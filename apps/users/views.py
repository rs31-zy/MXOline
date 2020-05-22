from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from apps.users.form import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next","")

        return render(request, 'login.html',{"next":next})
    def post(self,request,*args,**kwargs):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username = user_name,password = password)
            if user is not None:
                login(request,user)
                #取next值
                next = request.GET.get("next","")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html",{"msg":"用户名密码错误","login_form":login_form})
        else:
            return render(request, "login.html",{"login_form":login_form})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class UserInfoView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):


        return render(request,'usercenter-info.html')