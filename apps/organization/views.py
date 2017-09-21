# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .forms import UserAskForm
from .models import CourseOrg, CityDict
from operation.models import UserFavorite
# Create your views here.
import json


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3] # 取出3个

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort","")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-students')
            elif sort == "course":
                all_orgs = all_orgs.order_by('-course_nums')

        all_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)  # 每页的数量
        orgs = p.page(page)

        return render(request, 'org-list.html', {"all_orgs": orgs,
                                                 "all_citys": all_citys,
                                                 "all_nums": all_nums,
                                                 "city_id": city_id,
                                                 "category":category,
                                                 'hot_orgs':hot_orgs,
                                                 'sort':sort})


class AddUserAskView(View):
    '''用户添加咨询'''

    def post(self, request):
        ret_msg = {}
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form = userask_form.save(commit=True)  # 验证成功后，提交到数据库中保存
            ret_msg["status"] = "success"
            return HttpResponse(json.dumps(ret_msg))  # 返回json
        else:
            ret_msg["status"] = "fail"
            ret_msg["msg"] = "添加出错"
            return HttpResponse(json.dumps(ret_msg))


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = "home"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgCourseView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class AddFavView(View):
    '''用户收藏'''
    def post(self, request):
        ret_msg = {}
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', "")

        # 未登录,request.user是匿名
        if not request.user.is_authenticated():
            ret_msg["status"] = "fail"
            ret_msg["msg"] = "用户未登录"
            return HttpResponse(json.dumps(ret_msg))

        # 记录已经存在，则表示用户取消收藏
        exist_records = UserFavorite.objects.fileter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            exist_records.delete()
            ret_msg["status"] = "success"
            ret_msg["msg"] = "收藏"
            return HttpResponse(json.dumps(ret_msg))
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and fav_type > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = fav_type
                ret_msg["status"] = "success"
                ret_msg["msg"] = "已收藏"
                return HttpResponse(json.dumps(ret_msg))
            else:
                ret_msg["status"] = "fail"
                ret_msg["msg"] = "收藏出错"
                return HttpResponse(json.dumps(ret_msg))