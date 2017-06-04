# -*- coding: utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import xadmin
xadmin.autodiscover()
from django.views.static import serve #处理静态文件

from users.views import IndexView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView
from MxOnline.settings import MEDIA_ROOT
from filebrowser.sites import site
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    url(r'^filer/', include('filer.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),  
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name='login'),

    # 退出登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^register/$', RegisterView.as_view(), name='register'),

    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构 URL 配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关 URL 配置
    url(r'^course/', include('courses.urls', namespace='courses')),

    # 讲师相关 URL 配置
    url(r'^teacher/', include('courses.urls', namespace='teacher')),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    #配置 404，500 页面的静态文件访问处理
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # 用户中心 URL 配置
    url(r'^users/', include('users.urls', namespace='users')),

    # DjangoUeditor
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    
    # static resource
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,
        }),
]

# 全局 404 页面配置（django 会自动调用这个变量）
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        )
