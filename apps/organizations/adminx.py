import xadmin
from apps.organizations.models import City,Teacher,CourseOrg

class CityAdmin(object):
    list_display = ["id", "name", "descirption"]
    search_fields = ["name", "descirption"]
    list_filter = ["name", "descirption", "add_time"]
    list_editable = ["name", "descirption"]


class TeacherAdmin(object):
    list_display = ['org', 'name', 'years', 'company']
    search_fields = ['org', 'name', 'years', 'company']
    list_filter = ['org', 'name', 'years', 'company']

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    style_fields = {
        "desc": "ueditor"
    }

xadmin.site.register(City,CityAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)


