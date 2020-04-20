from django.contrib import admin
from file import models

# Register your models here.
class KindAdmin(admin.ModelAdmin):
    list_display = ('id','name','ctime',)
    list_display_links = ('id','name','ctime',)
    list_filter = ('name',)
    search_fields = ('name',)
    date_hierarchy = 'ctime'
admin.site.site_title = '文件分类表'  # 设置标题
admin.site.register(models.Kind,KindAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ('id','file_name','file_path','file_size','file_ip','file_hot','file_kind','file_time',)
    list_display_links = ('id','file_name','file_size','file_ip','file_hot','file_kind','file_time',)
    list_filter = ('file_kind__name','file_ip',)
    search_fields = ('file_name','file_kind__name','file_ip',)
    date_hierarchy = 'file_time'
    list_per_page = 15
admin.site.site_title = '文件表'  # 设置标题
admin.site.register(models.File,FileAdmin)