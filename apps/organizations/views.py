from django.shortcuts import render
from django.views.generic import View
from apps.organizations.models import CourseOrg, City, Teacher
# Create your views here.

class OrgView(View):
    def get(self,request,*args,**kwargs):

        #展示授课机构

        all_orgs = CourseOrg.objects.all()
        org_nums = CourseOrg.objects.all().count()
        all_citys = City.objects.all()


        return render(request,'org-list.html',{'all_orgs':all_orgs,'org_nums':org_nums,'all_citys':all_citys})
