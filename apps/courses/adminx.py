import xadmin
from apps.courses.models import Course
class CourseAdmin(object):

    list_display = ['id','name','desc','learn_times','degree']
    search_fields = ['name','desc']
    pass

xadmin.site.register(Course,CourseAdmin)