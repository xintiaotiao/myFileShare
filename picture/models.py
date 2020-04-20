from django.db import models

# Create your models here.

#创建用户表
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=32,verbose_name='用户名',unique=True)
    true_name = models.CharField(max_length=32,verbose_name='真实姓名',null=True,default='')
    password = models.CharField(max_length=32,verbose_name='密码')
    sex = models.IntegerField(choices=[(0, '男'), (1, '女'), ], default=1,verbose_name='性别')
    is_log = models.IntegerField(choices=[(1, '上线'), (2, '下线'), ], default=2, verbose_name='是否开启')
    phone = models.IntegerField(verbose_name='手机号码',null=True,default=888888)
    wx = models.CharField(max_length=32,verbose_name='微信号',null=True,default='')
    address = models.CharField(max_length=100,verbose_name='地址',null=True,default='')
    ctime = models.DateTimeField(auto_now=True,verbose_name='注册时间')

    class Meta:
        verbose_name_plural = '用户表管理'

    def __str__(self):
        return self.true_name

#创建图片表
class Pic(models.Model):
    id = models.AutoField(primary_key=True)
    pic_name = models.CharField(max_length=32,verbose_name='图集名称')
    pic_intro = models.CharField(max_length=32,verbose_name='图集简介',default='')
    pic_img = models.FileField(max_length=128,verbose_name='封面路径',upload_to='static/upload/%Y-%m-%d/',default='static/upload/%Y-%m-%d/')
    pic_use = models.IntegerField(choices=[(1, '上线'), (2, '下线'), ], default=1,verbose_name='是否启用')
    pic_kind = models.IntegerField(choices=[(1, '宽图'), (2, '方图'),(3, '长图'), ], default=1,verbose_name='图片类别')
    pic_hot = models.IntegerField(verbose_name='点击量',default=1)
    pic_weight = models.CharField(max_length=32,verbose_name='权重', default=1)
    pic_user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE,verbose_name='发布作者')
    ctime = models.DateTimeField(auto_now=True,verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '图片表管理'

    def __str__(self):
        return self.pic_name

#创建图片详情表
class PicDetail(models.Model):
    id = models.AutoField(primary_key=True)
    picd_name = models.CharField(max_length=32,verbose_name='图片名称')
    picd_kind = models.IntegerField(choices=[(1, '宽图'), (2, '方图'),(3, '长图'), ], default=1,verbose_name='图片类别')
    picd_use = models.IntegerField(choices=[(1, '上线'), (2, '下线'), ], default=1, verbose_name='是否启用')
    picd_weight = models.CharField(max_length=32,verbose_name='图片权重',default=1)
    picd_intro = models.CharField(max_length=128,verbose_name='图片介绍',default='')
    picd_img = models.ImageField(max_length=128,verbose_name='图片地址',upload_to='static/upload/%Y-%m-%d/',default='static/upload/%Y-%m-%d/')
    for_pic = models.ForeignKey(to='Pic',to_field='id',on_delete=models.CASCADE,verbose_name='所属图册')
    ctime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '图集表详情管理'

    def __str__(self):
        return self.picd_name

#定义相册评论表
class comment(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE,verbose_name='评论者',null=True)
    from_pic = models.ForeignKey(to='Pic', to_field='id',on_delete=models.CASCADE, verbose_name='所属相册')
    com_ip = models.GenericIPAddressField(max_length=32,verbose_name='评论者IP',default='127.0.0.1')
    content = models.TextField(verbose_name='评论内容')
    ctime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '图集评论表管理'

    def __str__(self):
        return self.content