#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Chenwei"
# Date: 2017/9/5

import xadmin
from xadmin import views
from models import EmailVerifyRecord, Banner

# Register your models here.


class BaseSetting(object):  # 修改主题
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):  # 修改全局配置
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = 'accordion'  # 折叠


class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_time", "send_type"]
    search_fields = ["code", "email", "send_type"]
    list_filter = ["code", "email", "send_type", "send_time"]


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", 'add_time']
    search_fields = ["title", "url", "index"]
    list_filter = ["title", "url", "index"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)# 全局注册方式
xadmin.site.register(views.CommAdminView, GlobalSetting)

