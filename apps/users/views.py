from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, JsonResponse

from apps.courses.models import Course
from apps.operations.models import UserFavorite
from apps.organizations.models import CourseOrg, Teacher
from apps.users.form import LoginForm, ChangePwdForm
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
        current_page = 'info'

        return render(request,'usercenter-info.html',{'current_page':current_page,
                                                      })


class MyFavOrgView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        current_page = 'myfavorg'
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        org_list = []
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{'current_page':current_page,
                                                         'org_list':org_list,
                                                         })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self,request,*args,**kwargs):
        current_page = 'myfavorg'
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        teacher_list = []
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{'current_page':current_page,
                                                             'teacher_list':teacher_list,
                                                             })



class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        current_page = 'myfavorg'
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_list = []
        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'current_page': current_page,
                                                              'course_list': course_list,
                                                               })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self,request,*args,**kwargs):
        pwd_form = ChangePwdForm(request.POST)

        if pwd_form.is_valid():
            pwd1 = request.POST.get('password1','')
            user = request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse(pwd_form.errors)
