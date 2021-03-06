# coding:utf-8
"""Mxonlie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
# from django.views.generic import TemplateView  # 处理静态文件
import xadmin
from users.views import IndexView
from django.views.static import serve

# from users.views import log_in
from users.views import LoginView, RegisterView, ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView, LogoutView
from organization.views import OrgView
from Mxonlie.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #  url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),  # 这样不用写views
    url(r'^$', IndexView.as_view(), name="index"),  # 这样不用写views
    url(r'^login/$', LoginView.as_view(), name="login"),  # 基于类的方式，别忘记as_view()后面的括号
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 基于类的方式，别忘记as_view()后面的括号
    url(r'^captcha/', include('captcha.urls')),  # 验证码
    url(r'^active/(?P<active_code>\.*)/$', ActiveUserView.as_view(), name="user_active" ),  # 取出验证链接后缀
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),  # 取出验证链接后缀
    url(r'^reset/(?P<active_code>\.*)/$', ResetView.as_view(), name="reset_pwd" ),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程
    url(r'^course/', include('course.urls', namespace="course")),

    # 用户个人信息
    url(r'^users/', include('users.urls', namespace="users")),

    # 配置上传文件路径
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # url(r'static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}), debug设置为false需要手动配置静态文件
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'  # 這个变量必须这样定义,记得把settins里面debug设置为false
handler500 = 'users.views.page_error'  # 這个变量必须这样定义,记得把settins里面debug设置为false