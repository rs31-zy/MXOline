from django.shortcuts import render
from django.views.generic import View
from apps.organizations.models import CourseOrg, City, Teacher
from pure_pagination import Paginator, PageNotAnInteger
from apps.organizations.form import AddAskForm
from django.http import JsonResponse

# Create your views here.

class OrgView(View):
    def get(self,request,*args,**kwargs):

        #展示授课机构

        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        org = request.GET.get("ct","")
        if org:
            all_orgs = all_orgs.filter(org = org)

        city_id = request.GET.get('city','')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        #对课程机构进行排序 减号代表倒序排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-student')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('lesson_nums')



        org_nums = all_orgs.count()


        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,per_page=5, request=request)
        orgs = p.page(page)


        return render(request,'org-list.html',{'all_orgs':orgs,
                                               'org_nums':org_nums,
                                               'all_citys':all_citys,
                                               'org':org,
                                               'city_id':city_id,
                                               'sort':sort,
                                               'hot_orgs':hot_orgs,
                                               })


class AddAsk(View):
    """处理用户咨询模块"""
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse({
                "status":"success",
                "msg":"提交成功"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })



class TeacherListView(View):
    def get(self,request,*args,**kwargs):
        all_teachers = Teacher.objects.all()

        teacher_nums = all_teachers.count()

        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-fav_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=5, request=request)
        teachers = p.page(page)

        return render(request,'teachers-list.html',{'teachers':teachers,
                                                    'teacher_nums':teacher_nums,
                                                    'hot_teachers':hot_teachers,
                                                    'sort':sort,

                                                    })
class TeacherDetailView(View):
    def get(self,request,teacher_id,*args,**kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        return render(request,'teacher-detail.html',{'teacher':teacher})
