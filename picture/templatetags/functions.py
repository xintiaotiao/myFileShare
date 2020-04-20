from django import template
from picture import models
from django.shortcuts import HttpResponse

register = template.Library()


# 通过id获取当前商品的评论信息
@register.filter(name='get_com_count') #模板中使用的自定义函数
def get_com_count(gid):
    count = models.comment.objects.filter(from_pic_id=gid).count()   #获取商品评论表中的总条数
    return count

#通过循环的比例判断商品存放的位置
@register.filter(name='img_position')
def img_position(forloop):
    res = int(forloop % 4)
    return res

#截取字符串函数
@register.filter(name='my_str') #模板中使用的自定义函数
def my_str(string):
    return string[10:]