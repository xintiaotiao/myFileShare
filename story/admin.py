from django.contrib import admin
from story  import models

# Register your models here.

#自定义后台管理-----------文章栏目表
class stoKindAdmin(admin.ModelAdmin):
    list_display = ('id','sto_kind','ctime',)
    list_display_links = ('id','sto_kind','ctime',)
    list_filter = ('sto_kind','ctime',)
    search_fields = ('sto_kind',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '文章分类表管理'  # 设置标题
admin.site.register(models.stoKind,stoKindAdmin)

#自定义后台管理-----------文章栏目表
class storyAdmin(admin.ModelAdmin):
    list_display = ('id','sto_name','sto_hot','sto_use','sto_weight','for_user','for_kind','sto_intro','ctime',)
    list_display_links = ('id','sto_name','sto_hot','sto_use','sto_weight','for_user','for_kind','sto_intro','ctime',)
    list_filter = ('for_kind__sto_kind','for_user__user_name','ctime',)
    search_fields = ('sto_name','for_kind_sto_kind','for_user__user_name')
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '文章栏目表管理'  # 设置标题
admin.site.register(models.story,storyAdmin)

#自定义后台管理-----------文章栏目表
class storyDetailAdmin(admin.ModelAdmin):
    list_display = ('id','stod_title','stod_use','stod_weight','for_story','ctime',)
    list_display_links = ('id','stod_title','stod_use','stod_weight','for_story','ctime',)
    list_filter = ('for_story__sto_name','ctime',)
    search_fields = ('stod_name','for_story__sto_name',)
    list_per_page = 15
    date_hierarchy = 'ctime'
admin.site.site_title = '文章栏目详情表管理'  # 设置标题
admin.site.register(models.storyDetail,storyDetailAdmin)