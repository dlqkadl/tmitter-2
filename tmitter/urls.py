"""Tmitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
import tmitter, django
from django.conf import settings
import django.contrib.syndication.views
import mvc.views

urlpatterns = [
    path(r'^$', mvc.views.index),    # 消息发布页面，主页
    path(r'^p/(?P<_page_index>\d+)/$', mvc.views.index_page),   # 消息发布页面，分页
    path(r'^user/$', mvc.views.index_user_self),                # 查看登录用户
    path(r'^user/(?P<_username>[a-zA-Z\-_\d]+)/$', mvc.views.index_user,
         name="tmitter-mvc-views-index_user"),                          # 查看制定用户
    path(r'^user/(?P<_username>[a-zA-Z\-_\d]+)/(?P<_page_index>\d+$',
         mvc.views.index_user_page),                            # 查看指定的用户消息分页
    path(r'^users/$', mvc.views.user_index),                    # 查看所有用户，朋友
    path(r'^users/(?P<_page_index>\d+/$',
         mvc.views.index_users_list),                           # 查看所有用户分页
    path(r'signin/$', mvc.views.signin),                        # 登录
    path(r'signup/$', mvc.views.signup),                        # 注册
    path(r'signout/$', mvc.views.signout),                      # 登出
    path(r'settings/$', mvc.views.settings,
         name='tmitter-mvc-views-settings'),                            # 修改登录用户的信息
    path(r'^message/(?P<_id>\d+)$', mvc.views.detail,
         name='tmitter-mvc-views-detail'),                              # 消息详情
    path(r'^message/(?P<_id>\d+)/delete/$',
         mvc.views.detail_delete,
         name='tmitter-mvc-views-detail_delete'),                       # 删除单条信息
    path(r'^friend/add/(?P<_username>[a-zA-Z\-_\d]+)',
         mvc.views.friend_add,
         name='tmitter-mvc-views-friend_add'),                          # 添加好友
    path(r'^friend/remove/(?P<_username>[a-zA-Z\-_\d]+)',
         mvc.views.friend_remove),                              # 删除好友
    path(r'^api/note/add/', mvc.views.api_note_add),            # 发布消息
    path('admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)       # 静态文件