from django.db import models

# Create your models here.

#创建一个文件类别表，用于检索条件
class Kind(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name='分类名称',unique=True)
    ctime = models.DateField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural ='文件分类表'
    def __str__(self):
        return self.name

#创建一个文件表，内容较多，可以把不常用字段拆分成2个表，做外键关联
class File(models.Model):
    id = models.AutoField(primary_key=True)
    file_name =models.CharField(max_length=32,verbose_name='文件名')
    file_path = models.FileField(max_length=128,verbose_name='下载地址',upload_to='static/upload/%Y-%m-%d/')
    file_size = models.CharField(max_length=32,verbose_name='文件大小',default= 'null')
    file_ip = models.CharField(max_length=32,verbose_name='上传者',default='127.0.0.1')
    file_hot = models.IntegerField(verbose_name='点击量',default=1)
    file_kind = models.ForeignKey(to='Kind',to_field='id',verbose_name='文件类别',on_delete=models.CASCADE)
    file_intro = models.TextField(max_length=64,verbose_name='文件介绍',default='作者：心跳跳')
    file_time = models.DateTimeField(auto_now_add=True,verbose_name='上传时间')

    class Meta:
        verbose_name_plural ='文件表'
    def __str__(self):
        return self.file_name