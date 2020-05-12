from django.conf.urls import url
from apps.courses.views import CourseView,CourseDetailView

urlpatterns =[
    url(r'^list/$', CourseView.as_view(), name="list"),
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
]