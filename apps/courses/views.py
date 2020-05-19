from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course, Video, CourseResource, CourseTag
from pure_pagination import Paginator, PageNotAnInteger
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from django.contrib.auth.mixins import LoginRequiredMixin
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
        #获取收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                has_fav_org = True

        #课程推荐
        #通过课程的单标签进行推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]

        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        related_courses = []
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        for course_tag in course_tags:
            related_courses.append(course_tag.course)


        return render(request,'course-detail.html',{'course':course,
                                                    'has_fav_course':has_fav_course,
                                                    'has_fav_org':has_fav_org,
                                                    'related_courses':related_courses,
                                                    })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self,request,course_id,*args,**kwargs):
        course = Course.objects.get(id = int(course_id))
        #查询资料

        course.click_nums += 1
        course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[0:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)



        course_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html',{'course':course,
                                                    'course_resource':course_resource,
                                                    'related_courses':related_courses,
                                                    })


class CourseCommentsView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,course_id,*args,**kwargs):
        course = Course.objects.get(id=int(course_id))
        # 查询资料

        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[0:5]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-comment.html', {'course': course,
                                                       'course_resource': course_resource,
                                                       'related_courses': related_courses,
                                                       'comments': comments,
                                                       })
