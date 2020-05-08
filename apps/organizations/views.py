from django.shortcuts import render
from django.views.generic import View
from apps.organizations.models import CourseOrg, City, Teacher
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class OrgView(View):
    def get(self,request,*args,**kwargs):

        #展示授课机构

        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()

        org = request.GET.get("ct","")
        if org:
            all_orgs = all_orgs.filter(org = org)

        city_id = request.GET.get('city','')
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        org_nums = all_orgs.count()


        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,per_page=5, request=request)
        orgs = p.page(page)


        return render(request,'org-list.html',{'all_orgs':orgs,'org_nums':org_nums,'all_citys':all_citys,'org':org,'city_id':city_id,})
