from django.shortcuts import render
from django.views.generic.base import View
from apps.operations.form import UserFavForm, CommentForm
from django.http import JsonResponse
from apps.operations.models import UserFavorite, CourseComments
from apps.courses.models import Course
from apps.organizations.models import CourseOrg
from apps.organizations.models import Teacher

# Create your views here.


class AddFavView(View):
    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg' : '用户未登录',
            })
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            fav_type = user_fav_form.cleaned_data['fav_type']
            #判断用户是否已收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                # 收藏这条信息删除
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    cousre_org = CourseOrg.objects.get(id=fav_id)
                    cousre_org.fav_nums -= 1

                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse(
                    {"status": "success",
                     "msg": "收藏"}
                )
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse(
                    {"status": "success",
                     "msg": "已收藏"}
                )

        else:
            return JsonResponse(
                {"status": "fail",
                 "msg": "参数错误"}
            )

class CommentView(View):
    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail',
                                 'msg' : '用户未登录',
                                 })
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            comment = CourseComments()
            comment.user = request.user
            comment.course = course
            comment.comments = comments
            comment.save()
            return JsonResponse({"status": "success",
                                 })
        else:
            return JsonResponse({'status': 'fail',
                                 'msg': '参数错误',
                                 })



