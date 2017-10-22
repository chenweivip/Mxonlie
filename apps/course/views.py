# coding:utf-8

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from models import Course, CourseResource
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
import json

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))
        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by('-students')
            elif sort == "hot":
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)  # 每页的数量
        courses = p.page(page)
        return render(request, 'course-list.html', {"all_courses":courses,
                                                    'sort':sort,
                                                    "hot_courses":hot_courses})


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  # 增加课程点击数
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag  # 技术点 添加一个标签,关联课程
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,'course-detail.html', {"course": course,
                                                    'relate_courses': relate_courses,
                                                    "has_fav_course": has_fav_course,
                                                    "has_fav_org": has_fav_org,
                                                    })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.all()
        return render(request, 'course-comment.html', {
            "course": course,
            'course_resources': all_resources,
            'course_comments': all_comments,
        })


class AddCommentsView(View):
    def post(self, request):
        ret_msg = {}
        if not request.user.is_authenticated():
            ret_msg["status"] = "fail"
            ret_msg["msg"] = "用户未登录"
            return HttpResponse(json.dumps(ret_msg))
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            ret_msg["status"] = "success"
            ret_msg["msg"] = "添加成功"
            return JsonResponse(ret_msg)
        else:
            ret_msg["status"] = "fail"
            ret_msg["msg"] = "添加失败"
            return HttpResponse(json.dumps(ret_msg))