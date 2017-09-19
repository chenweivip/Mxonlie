#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Chenwei"
# Date: 2017/9/19

from operation.models import UserAsk
from django import forms
import re


class UserAskForm(forms.ModelForm): # modelform = model + form
    class Meta:
        model = UserAsk  # 将model转换为form
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        :return: 
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invalid")