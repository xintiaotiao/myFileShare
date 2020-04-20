from django.contrib import admin
from picture import models

# Register your models here.

#自定义后台管理-----------用户表
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','user_name','true_name','sex','is_log','phone','wx','address','ctime',)
    list_display_links = ('id','user_name','true_name','sex','is_log','phone','wx','address','ctime',)
    list_filter = ('sex','ctime',)
    search_fields = ('user_name','true_name','sex','address',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '用户表管理'  # 设置标题
admin.site.register(models.User,UserAdmin)

#自定义后台管理-----------图片表
class PicAdmin(admin.ModelAdmin):
    list_display = ('id','pic_name','pic_intro','pic_kind','pic_use','pic_img','pic_hot','pic_weight','pic_user','ctime',)
    list_display_links = ('id','pic_name','pic_intro','pic_kind','pic_use','pic_hot','pic_weight','pic_user','ctime',)
    list_filter = ('pic_user','pic_kind','pic_use','ctime',)
    search_fields = ('pic_name','pic_intro','pic_user__user_name',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '图片表管理'  # 设置标题
admin.site.register(models.Pic,PicAdmin)

#自定义后台管理-----------图片详情表
class PicDetailAdmin(admin.ModelAdmin):
    list_display = ('id','picd_name','picd_intro','picd_kind','picd_use','picd_img','picd_weight','for_pic','ctime',)
    list_display_links = ('id','picd_name','picd_intro','picd_kind','picd_use','picd_img','picd_weight','for_pic','ctime',)
    list_filter = ('for_pic','picd_kind','picd_use','ctime',)
    search_fields = ('picd_name','picd_intro','for_pic__pic_name',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '图片详情表管理'  # 设置标题
admin.site.register(models.PicDetail,PicDetailAdmin)

#自定义后台管理-----------相册评论表
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','content','from_user','from_pic','com_ip','ctime',)
    list_display_links = ('id','content','from_user','from_pic','com_ip','ctime',)
    list_filter = ('from_user__user_name','from_pic__pic_name',)
    search_fields = ('from_user__user_name','from_pic__pic_name','content',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '图册评论表管理'  # 设置标题
admin.site.register(models.comment,CommentAdmin)
admin.site.site_header = 'Foxconn管理后台'
