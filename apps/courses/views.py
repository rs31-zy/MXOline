from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self,request,*args,**kwargs):
        all_courses = Course.objects.all()

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,per_page=4, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{'all_courses':courses})

