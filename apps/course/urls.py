#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Chenwei"
# Date: 2017/9/21

from django.conf.urls import url
from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程列表首页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

]