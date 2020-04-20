"""foxconn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
#导入图集views函数
from picture   import views as pic_views
#导入文学views函数
from story  import views as sto_views
#导入文件views函数
from file import views as file_views

urlpatterns = [

    #图片墙功能路由集合-------------------------------------------------------------------------------------------
    path('admin/', admin.site.urls),
    #配置图片网址的首页地址路由
    # re_path('^$',pic_views.pic_index),
    re_path('$^',file_views.index),
    re_path('pic_index.html$',pic_views.pic_index),
    #配置用户注册路由
    re_path('register.html$',pic_views.register),
    #配置用户名验证路由
    re_path('check_user.html$',pic_views.check_user),
    # 配置用户登录路由
    re_path('login.html$', pic_views.login),
    # 配置用户退出路由
    re_path('logout.html$', pic_views.logout),
    #后台首页路由-图片墙
    re_path('my_admin',pic_views.my_admin),
    #我要上传图片
    re_path('pic_upload.html$',pic_views.pic_upload),
    #处理图片上传路由
    re_path('pic_upload_data.html$',pic_views.pic_upload_data),
    #编辑图片路由
    re_path('pic_edit.html$',pic_views.pic_edit),
    #删除图片路由
    re_path('pic_del.html$',pic_views.pic_del),
    #图集详细信息列表
    re_path('picd_list.html$',pic_views.picd_list),
    #图集详细信息添加路由
    re_path('picd_add.html$',pic_views.picd_add),
    # 图集详细信息数据添加路由
    re_path('picd_add_data.html$', pic_views.picd_add_data),
    # 图集详细信息数据添加路由
    re_path('picd_edit.html$', pic_views.picd_edit),
    # 删除详情图片路由
    re_path('picd_del.html$', pic_views.picd_del),
    # 图集评论表路由
    re_path('pic_index_new.html$', pic_views.pic_index_new),
    #图集评论表删除功能
    re_path('com_del.html$',pic_views.com_del),
    #图集评论入库功能
    re_path('com_data.html',pic_views.com_data),
    #图集点击自动增加路由
    re_path('pic_hot_add.html$',pic_views.pic_hot_add),
    #我的个人资料路由
    re_path('my_info.html$',pic_views.my_info),
    #用户资料编辑
    re_path('user_edit.html$',pic_views.user_edit),

    #文学表路由控制集合------------------------------------------------------------------------------------------------
    #文学网首页路由
    re_path('story_index.html',sto_views.story_index),
    #文章点击自动增加
    re_path('sto_hot_add.html',sto_views.sto_hot_add),
    # 文章首页详情页面1
    re_path('story_index_list.html', sto_views.story_index_list),
    #文章首页详情页面
    re_path('story_index_detail.html',sto_views.story_index_detail),
    #文学网后台管理首页
    re_path('my_story.html$',sto_views.my_story),
    #文学添加界面
    re_path('story_add.html$',sto_views.story_add),
    # 文学添加数据处理
    re_path('story_add_data.html$', sto_views.story_add_data),
    #文学编辑界面
    re_path('story_edit.html$',sto_views.story_edit),
    #文学详情展示界面
    re_path('story_detail_list.html',sto_views.story_detail_list),
    # 文学详情添加界面
    re_path('story_detail_add.html', sto_views.story_detail_add),
    #文学章节添加数据处理
    re_path('story_detail_add_data.html',sto_views.story_detail_add_data),
    #文章章节编辑界面展示
    re_path('story_detail_edit.html',sto_views.story_detail_edit),
    #文章章节删除
    re_path('story_detail_del.html',sto_views.story_detail_del),
    #文章删除
    re_path('story_del.html',sto_views.story_del),

#文件表路由控制集合------------------------------------------------------------------------------------------------
    re_path('index.html$', file_views.index),  # 定义文件馆首页路由
    re_path('download.html$', file_views.download),
    re_path('upload.html$', file_views.upload),
    re_path('file_del.html$',file_views.file_del),

#网络爬虫测试，自动登录、自动评论功能实现
    re_path('pachong',file_views.pachong),
    re_path('py_requests',file_views.py_requests),


]
