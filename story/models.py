from django.db import models
from picture.models import User

# Create your models here.

#创建文学分类表
class stoKind(models.Model):
    id = models.AutoField(primary_key=True)
    sto_kind = models.CharField(max_length=32,unique=True,verbose_name='文学分类名')
    ctime = models.DateTimeField(auto_now=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '文学分类表管理'

    def __str__(self):
        return self.sto_kind

#创建文学栏目表
class story(models.Model):
    id = models.AutoField(primary_key=True)
    sto_name = models.CharField(max_length=32,verbose_name='文章名称')
    sto_img =  models.ImageField(max_length=128,verbose_name='图片地址',upload_to='static/upload/%Y-%m-%d/')
    sto_hot = models.IntegerField(verbose_name='点击量')
    sto_weight = models.IntegerField(verbose_name='文章排序')
    sto_use = models.IntegerField(choices=((0,'上线'),(1,'下线'),),verbose_name='是否上线')
    sto_sort = models.CharField(max_length=32,verbose_name='排序随机字段',default='a',db_index=True)
    for_kind = models.ForeignKey(to='stoKind',to_field='id',on_delete=models.CASCADE,verbose_name='所属类别')
    for_user = models.ForeignKey(to='picture.User',to_field='id',on_delete=models.CASCADE,verbose_name='发布者',default=1)
    ctime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    sto_intro = models.TextField(verbose_name='文章简介')

    class Meta:
        verbose_name_plural = '文学栏目表管理'

    def __str__(self):
        return self.sto_name

#创建文学栏目详情表
class storyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    stod_title = models.CharField(max_length=32,verbose_name='文章标题')
    stod_weight = models.CharField(max_length=32,verbose_name='排序')
    stod_use = models.IntegerField(choices=((0,'上线'),(1,'下线'),),verbose_name='是否上线')
    for_story = models.ForeignKey(to='story',to_field='id',on_delete=models.CASCADE,verbose_name='所属文章')
    ctime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    stod_content = models.TextField(verbose_name='文章内容')

    class Meta:
        verbose_name_plural = '文学栏目详情表管理'

    def __str__(self):
        return self.stod_title