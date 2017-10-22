#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Chenwei"
# Date: 2017/9/21

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentsView

urlpatterns = [
    # 课程列表首页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_commet"),

    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_commet"),


]