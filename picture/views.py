from django.shortcuts import render,HttpResponse,redirect
from picture import models
import json,time,os,random
from django.db.models import F,Q

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.

#图片墙首页路由
def pic_index(request):
    # return  HttpResponse('pic')
    #获取轮播图图片，以权重、热度进行排序
    data = models.Pic.objects.filter(pic_use = 1).values('id','pic_name','pic_user__true_name','pic_kind','pic_img').order_by('-pic_weight','-pic_hot')[0:10]
    # print(data)
    #图片墙显示功能代码
    # 获取搜索条件
    search = request.GET.get('search')
    # kind = request.GET.get('kind')
    # print(search)
    #生成列表
    if search:
        # 获取图集中要展示的数据
        data_list = models.Pic.objects.filter(Q(pic_name__regex=search) | Q(pic_user__true_name__regex=search)).filter(pic_use = 1).values('id', 'pic_name','pic_user__true_name','pic_hot', 'pic_intro', 'pic_img', 'ctime').order_by('-pic_hot')
    else:
        # 获取图集中要展示的数据
        data_list = models.Pic.objects.filter(pic_use = 1).values('id', 'pic_name','pic_user__true_name', 'pic_hot',  'pic_intro', 'pic_img', 'ctime').order_by('-pic_hot')
    # print(data_list)

    # 分页
    from picture import pager
    current_page = request.GET.get('p', 1)
    pager = pager.Pagination('pic_index.html', len(data_list), current_page, 50)
    pic_data = data_list[pager.start():pager.end()]

    return render(request,'picture/index.html',{'data':data,'pic_data':pic_data,'pager':pager,'search':search})

#图集点击后自动增加
def pic_hot_add(request):
    #获取ajax传递的值
    id = request.GET.get('pid')
    # print(id)
    models.Pic.objects.filter(id = id).update(pic_hot = F('pic_hot')+1)
    return HttpResponse('success')

#图册评论表功能
def pic_index_new(request):
    #获取要评论的图册id
    id = request.GET.get('id')
    #获取当前图册内的详细图片信息
    pic_path = models.PicDetail.objects.filter(for_pic__id = id).values('picd_name','picd_intro','picd_kind','picd_img').order_by('picd_weight')
    data = models.Pic.objects.filter(id = id).values('id','pic_name','pic_intro','pic_user__true_name','pic_user__sex', \
     'pic_user__phone','pic_user__wx','pic_user__address','pic_user__ctime',  ).first()
    # print(data)
    #获取当前图册的评论信息
    com_data = models.comment.objects.filter(from_pic__id = id).values('from_user__id','from_user__true_name','id','com_ip','ctime','content').order_by('-ctime')[0:66]
    # print(com_data)
    # return  HttpResponse("comment success" )
    return render(request,'picture/pic_detail.html',{"pic_path":pic_path,'data':data,"com_data":com_data})

#删除评论功能
def com_del(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #获取要删除评论的id
    id = request.GET.get('id')
    pid = request.GET.get('pid')
    models.comment.objects.filter(id = id).delete()
    return redirect('/pic_index_new.html?id=%s' %(pid))

#图集评论功能代码
def com_data(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #获取ajax发送的评论信息
    get = request.GET
    # print(get)
    from_pic = models.Pic.objects.get(id = get['pic_id'])
    from_user = models.User.objects.get(id = request.session.get('user_id'))
    com_ip = request.META['REMOTE_ADDR']  # 获取META数组，获取其中的ip地址
    content = get['content']
    com_time = time.strftime('%Y-%m-%d %X')  # 格式化日期时间
    dic_list = {"from_pic": from_pic, "from_user": from_user, "com_ip": com_ip, "content": content,
                "ctime": com_time}
    # print(dic_list)
    #实现数据入库
    models.comment.objects.create(**dic_list)
    return HttpResponse('success')

#用户注册代码功能
def register(request):
    try:
        #接收ajax传递的数据
        post = request.POST
        # print(post)
        #组装字典，
        dic_data = {"is_log":2,"user_name":post['username'],"password":post['password'],"true_name":post['truename'],"phone":post['phone'],"wx":post['weixin'],"address":post['address'],"sex":post['sex'],}
        # print(dic_data)
        #实现注册数据进数据库
        models.User.objects.create(**dic_data)
        return HttpResponse(json.dumps({"code": 0, "message": '恭喜，注册成功！'}))
    except Exception as e: #采取抛出异常机制
        return HttpResponse(json.dumps({"code": 1, "message": str(e)}))

#验证用户名是否可用路由
def check_user(request):
    username = request.GET.get('username')
    #在数据库验证用户名
    if  models.User.objects.filter(user_name = username):
       return HttpResponse("<span style='color:red'>%s:此用户名已被注册，请更换！</span>" %(username))
    else:
        return HttpResponse("<span style='color:blue'>%s:此用户名未注册，请注册！</span>" % (username))


#用户登录代码能够
def login(request):
    try:
        #获取ajax发送的信息
        get = request.GET
        # print(get)
        data =  models.User.objects.filter(user_name = get['username2'],password = get['password2'],is_log = 1).values('id','user_name','true_name').first()
        if data :
            request.session['user_id'] = data['id']
            request.session['user_name'] = data['user_name']
            request.session['true_name'] = data['true_name']
            return HttpResponse(json.dumps({"code": 0, "message": 'success'}))
        else:
            return HttpResponse(json.dumps({"code": 1, "message": '您的账号未启用，或用户名、密码错误，请联系管理员！'}))
    except Exception as e :
        return HttpResponse(json.dumps({"code": 1, "message": str(e)}))


# 用户退出代码能够
def logout(request):
    #清空session
    request.session.flush()
    #跳转到图片墙首页
    return redirect('pic_index.html')

#后台首页，后台所有功能必须登录后才能访问，所以都要加一个session判断
def my_admin(request):

    #判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #获取搜索条件
    search = request.GET.get('search')
    if search :
        # 获取图集中要展示的数据
        data_list = models.Pic.objects.filter(pic_user__id=request.session.get('user_id'),pic_name__regex=search).values('id', 'pic_name','pic_kind','pic_use',
                                                                                                  'pic_hot',
                                                                                                  'pic_weight',
                                                                                                  'pic_intro',
                                                                                                  'pic_img', 'ctime');
    else:
        # 获取图集中要展示的数据
        data_list = models.Pic.objects.filter(pic_user__id=request.session.get('user_id')).values('id', 'pic_name','pic_kind','pic_use',
                                                                                                  'pic_hot',
                                                                                                  'pic_weight',
                                                                                                  'pic_intro',
                                                                                                  'pic_img', 'ctime');

    # print(data_list)

    #分页
    from picture import pager
    current_page = request.GET.get('p', 1)
    pager = pager.Pagination('my_admin', len(data_list), current_page,30)
    data = data_list[pager.start():pager.end()]

    return render(request,'picture/my_admin.html',{"pager":pager,'data':data,'search':search})

#上传图片功能代码
def pic_upload(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    return render(request,'picture/pic_upload.html')

#处理上传图片的数据和编辑功能融合一体
def pic_upload_data(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    post = request.POST
    file = request.FILES.get('pic_file')
    # print(post,'---',file)
    #判断是否有文件上传
    if file:
        #配置文件上传的路径
        if not os.path.isdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d')):
            os.mkdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d'))
        upload_path = 'static/upload/' + time.strftime('%Y-%m-%d') + '/' + str(
            random.randrange(1000, 9999)) + '_' + file.name
        # print(upload_path)
        #写入指定路径的文件
        f = open(upload_path, 'wb')
        # f = open('%Y-%m-%d.jpg','wb')
        for chunks in file.chunks(1024):
            f.write(chunks)
        f.close()
    #判断传递的是否存在get方式中的id参数，如果存在表示为编辑，否则为新增
    id = request.GET.get('id')
    if id:
        #定义编辑的字典
        ctime = time.strftime('%Y-%m-%d %X')  # 格式化日期时间
        if file:
            dic_data = {"pic_name": post['pic_name'], "pic_intro": post['pic_intro'],"pic_use":post['pic_use'], "pic_img": upload_path,"pic_kind": post['pic_kind']}
        else:
            dic_data = {"pic_name": post['pic_name'], "pic_intro": post['pic_intro'],"pic_use":post['pic_use'], "pic_kind": post['pic_kind']}
        #根据id修改数据
        print(dic_data)
        models.Pic.objects.filter(id = id).update(**dic_data)

    else:
        #定义写入数据库的字典
        pic_user = models.User.objects.get(id=request.session.get('user_id'))  # 外键关联不能直接写值，必须是一个外键对象
        ctime = time.strftime('%Y-%m-%d %X')  # 格式化日期时间
        dic_data = {"pic_name":post['pic_name'],"pic_intro":post['pic_intro'],"pic_use":post['pic_use'],"pic_img":upload_path,"pic_hot":1,"pic_weight":1,"pic_user":pic_user,"ctime":ctime,"pic_kind":post['pic_kind']}
        # print(dic_data)
        models.Pic.objects.create(**dic_data)
    return redirect('/my_admin')

#跳转到图片编辑界面
def pic_edit(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #根据传递的id查询要修改图集的信息
    id = request.GET.get('id')
    data = models.Pic.objects.filter(id = id).values().first()
    return render(request,'picture/pic_edit.html',{'data':data})

#删除图片墙图片
def pic_del(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #根据传递的id查询要修改图集的信息
    id = request.GET.get('id')
    #同时删除详细图片信息
    #先删除文件路径，后删除记录
    del_path = models.PicDetail.objects.filter(for_pic__id=id).values('picd_img')
    for item in del_path:
        if os.path.exists(BASE_DIR + '/' + item['picd_img']):
            os.remove(BASE_DIR + '/' + item['picd_img'])
    models.PicDetail.objects.filter(for_pic__id = id).delete()
    #首先判断要删除的文件是否存在，存在则删除
    dic = models.Pic.objects.filter(id=id).values('pic_img').first()
    if os.path.exists(BASE_DIR + '/' + dic['pic_img']):
        os.remove(BASE_DIR + '/' + dic['pic_img'])
    models.Pic.objects.filter(id = id).delete()
    return redirect('/my_admin')

#为图册添加详细图片信息
def picd_list(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #通过传递的图集id获取该图集对应的详细图片描述
    id = request.GET.get('id')
    #获取要添加的图册名称
    name = models.Pic.objects.filter(id = id).values('id','pic_name').first()
    data = models.PicDetail.objects.filter(for_pic__id = id).values()
    # print(name)
    return render(request,'picture/picd_list.html',{'data':data,'name':name['pic_name'],'id':id})

#为商品详细信息功能代码
def picd_add(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #获取传递过来的信息,只是用来展示添加页面
    pid = request.GET.get('pid')
    return render(request,'picture/picd_add.html',{'pid':pid})

#为商品详细信息功能代码
def picd_add_data(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    pid = request.GET.get('pid')
    post = request.POST
    file = request.FILES.get('picd_file')
    # print(post,'---',file,'--',pid)
    # 判断是否有文件上传
    if file:
        # 配置文件上传的路径
        if not os.path.isdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d')):
            os.mkdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d'))
        upload_path = 'static/upload/' + time.strftime('%Y-%m-%d') + '/' + str(
            random.randrange(1000, 9999)) + '_' + file.name
        # print(upload_path)
        # 写入指定路径的文件
        f = open(upload_path, 'wb')
        # f = open('%Y-%m-%d.jpg','wb')
        for chunks in file.chunks(1024):
            f.write(chunks)
        f.close()
    # 判断传递的是否存在get方式中的id参数，如果存在表示为编辑，否则为新增
    id = request.GET.get('id')
    if id:
        # 定义编辑的字典
        if file:
            dic_data = {"picd_name": post['picd_name'], "picd_intro": post['picd_intro'], "picd_use": post['picd_use'],
                    "picd_img": upload_path,"picd_weight": post['picd_weight'],
                    "picd_kind": post['picd_kind']}
        else:
            dic_data = {"picd_name": post['picd_name'], "picd_intro": post['picd_intro'], "picd_use": post['picd_use'],"picd_weight": post['picd_weight'],
                    "picd_kind": post['picd_kind']}
        # 根据id修改数据
        # print(dic_data)
        models.PicDetail.objects.filter(id=id).update(**dic_data)

    else:
        # 定义写入数据库的字典
        for_pic = models.Pic.objects.get(id=pid)  # 外键关联不能直接写值，必须是一个外键对象
        dic_data = {"picd_name": post['picd_name'], "picd_intro": post['picd_intro'], "picd_use": post['picd_use'],
                    "picd_img": upload_path,"picd_weight": post['picd_weight'], "for_pic": for_pic,
                    "picd_kind": post['picd_kind']}
        # print(for_pic)
        # print(dic_data)
        models.PicDetail.objects.create(**dic_data)
    return redirect('picd_list.html?id=' + str(pid))

#展示图片详情编辑界面
def picd_edit(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    # 根据传递的id查询要修改图集的信息
    id = request.GET.get('id')
    pid = request.GET.get('pid')

    # del_path = models.PicDetail.objects.filter(for_pic__id=pid).values('picd_img')
    # print(del_path)

    data = models.PicDetail.objects.filter(id = id).values().first()
    # print(data)
    return render(request, 'picture/picd_edit.html', {'data': data,'pid':pid})

#删除详情图片墙图片
def picd_del(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #根据传递的id查询要修改图集的信息
    id = request.GET.get('id')
    pid = request.GET.get('pid')
    #首先判断要删除的文件是否存在，存在则删除
    dic = models.PicDetail.objects.filter(id=id).values('picd_img').first()
    # print(dic)
    if os.path.exists(BASE_DIR + '/' + dic['picd_img']):
        os.remove(BASE_DIR + '/' + dic['picd_img'])
    models.PicDetail.objects.filter(id = id).delete()
    return redirect('picd_list.html?id=' + str(pid))

#我的资料展示界面
def my_info(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    #查询当前用户的信息，并分配数据
    data = models.User.objects.filter(id = request.session.get('user_id')).values().first()
    # print(data)
    return render(request,'picture/my_info.html',{"data":data})

def user_edit(request):
    # 判断session中的user_id,如果不存在则跳转到登录界面
    if not request.session.get('user_id'):
        return HttpResponse('您还未登录，请先登录！')
    try:
        # 接收ajax传递的数据
        post = request.GET
        # print(post)
        if post['p'] and post['ph'] and post['t'] and post['w'] and post['ad']:
            # 组装字典，
            dic_data = {"password": post['p'], "true_name": post['t'],
                        "phone": post['ph'], "wx": post['w'], "address": post['ad'],"sex":post['sex1']}
            # print(dic_data)
            # 实现注册数据进数据库
            models.User.objects.filter(id = request.session.get('user_id')).update(**dic_data)
            return HttpResponse(json.dumps({"code": 0, "message": '恭喜，修改成功！'}))
        else:
            return HttpResponse(json.dumps({"code": 1, "message": "所有栏目不能为空！"}))
    except Exception as e:  # 采取抛出异常机制
        return HttpResponse(json.dumps({"code": 1, "message": str(e)}))