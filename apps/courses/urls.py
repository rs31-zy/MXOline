from django.conf.urls import url
from apps.courses.views import CourseView

urlpatterns =[
    url(r'^list/$', CourseView.as_view(), name="list"),

]