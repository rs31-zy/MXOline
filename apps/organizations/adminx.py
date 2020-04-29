import xadmin
from apps.organizations.models import City,Teacher,CourseOrg

class CityAdmin(object):
    list_display = ['id', 'name', 'descirption']
    pass


class TeacherAdmin(object):
    list_display = ['id', 'name', 'age',  'years', 'company', 'post']
    pass

class CourseOrgAdmin(object):
    list_display = ['id', 'name', 'tag',  'category', 'org', 'attestation', 'gold']
    pass


xadmin.site.register(City,CityAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)


