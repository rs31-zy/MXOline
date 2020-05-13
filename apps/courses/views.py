from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from apps.operations.models import UserFavorite
# Create your views here.


class CourseView(View):
    def get(self,request,*args,**kwargs):
        all_courses = Course.objects.order_by('-add_time')
        hot_courses = all_courses.order_by("-students")[:3]

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-students')
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
                                                  'hot_courses':hot_courses,
                                                  })

class CourseDetailView(View):
    def get(self,request,course_id,*args,**kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                has_fav_org = True


        return render(request,'course-detail.html',{'course':course,
                                                    'has_fav_course':has_fav_course,
                                                    'has_fav_org':has_fav_org
                                                    })

