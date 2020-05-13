from django.db import models

# Create your models here.
from apps.users.models import BaseModel
from apps.users.models import UserProfile

class City(BaseModel):
    name = models.CharField(verbose_name="城市名",max_length=20)
    descirption = models.CharField(verbose_name="描述",max_length=200)

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    city = models.ForeignKey(City, verbose_name="所在城市", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="机构名称",max_length=20)
    tag = models.CharField(verbose_name="机构标签",max_length=20,default="")
    category = models.CharField(verbose_name="机构类别", max_length=20, default="")
    org = models.CharField(verbose_name="培训机构", choices=(('gr', "个人"), ('gx', "高校")), max_length=2)
    click_nums = models.IntegerField(verbose_name="点击人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏人数", default=0)
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(verbose_name="机构地址", max_length=50)
    student = models.IntegerField(verbose_name="学习人数", default=0)
    lesson_nums = models.IntegerField(verbose_name="课程数",default=0)
    attestation = models.BooleanField(default=False, verbose_name="是否认证")
    desc = models.CharField(max_length=200, verbose_name=u"描述",default="")
    gold = models.BooleanField(default=False, verbose_name="是否金牌")

    def courses(self):
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(verbose_name="教师姓名", max_length=10)
    years = models.IntegerField(default=0, verbose_name="工作年限")
    company = models.CharField(verbose_name="就职公司",max_length=50)
    post = models.CharField(verbose_name="公司职位",max_length=10)
    teach_feature = models.CharField(verbose_name="教学特点",max_length=50)
    click_nums = models.IntegerField(verbose_name="点击人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏人数", default=0)
    age = models.IntegerField(default=0, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)


    def course_nums(self):
        return self.course_set.all().count()
    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



