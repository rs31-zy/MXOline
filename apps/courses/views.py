from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self,request,*args,**kwargs):
        all_courses = Course.objects.order_by('-add_time')
        hot_courses = all_courses.order_by("-student")[:3]

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-student')
        elif sort == 'students':
            all_courses = all_courses.order_by('click_nums')

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,per_page=3, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{'all_courses':courses,
                                                  'sort':sort,
                                                  'hot_courses':hot_courses
                                                  })

