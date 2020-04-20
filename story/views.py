from django.shortcuts import render,redirect,HttpResponse
from story import models
import json,time,os,random
from story.code import genRandomString
from django.db.models import F,Q
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#文学网首页路由
def story_index(request):
    #获取文章分类信息id
    id = request.GET.get('id',0)
    #获取搜索信息
    search = request.GET.get('search','')
    # print(id)
    #获取文学分类信息，并分配数据到模板
    kind = models.stoKind.objects.values('id','sto_kind')
    if search:
        if id :
            # 获取要文章数据
            data_list = models.story.objects.filter(Q(sto_name__regex=search) | Q(for_user__true_name__regex=search)).filter(
                sto_use=0,for_kind__id=id).values('id', 'sto_name', 'sto_img', 'sto_hot', 'sto_intro',
                                  'for_kind__sto_kind', 'for_user__true_name').order_by(
                 '-sto_hot')
        else:
            # 获取要文章数据
            data_list = models.story.objects.filter(Q(sto_name__regex=search) | Q(for_user__true_name__regex=search)).filter(
                sto_use=0).values('id', 'sto_name', 'sto_img', 'sto_hot', 'sto_intro',
                                                   'for_kind__sto_kind', 'for_user__true_name').order_by(
               '-sto_hot')
    else:
        if id:
            # 获取要文章数据
            data_list = models.story.objects.filter(sto_use=0,for_kind__id=id).values('id', 'sto_name', 'sto_img', 'sto_hot', 'sto_intro',
                                                                      'for_kind__sto_kind', 'for_user__true_name').order_by(
               '-sto_hot')
        else:
            # 获取要文章数据
            data_list = models.story.objects.filter(sto_use=0).values('id', 'sto_name', 'sto_img',
                                                                                       'sto_hot', 'sto_intro',
                                                                                       'for_kind__sto_kind',
                                                                                       'for_user__true_name').order_by(
                 '-sto_hot')

    # 分页
    from picture import pager
    current_page = request.GET.get('p', 1)
    pager = pager.Pagination('story_index.html', len(data_list), current_page, 50, id=id,search=search)
    data = data_list[pager.start():pager.end()]
    # print(data)
    return render(request,'story/story_index.html',{'kind':kind,"id":id,"search":search,"data":data,"pager":pager})

#文章点击自动增加
def sto_hot_add(request):
    #获取文章的id
    id = request.GET.get('id')
    models.story.objects.filter(id=id).update(sto_hot=F('sto_hot')+1)
    return  HttpResponse(id)

#文章首页详细页面功能1
def story_index_list(request):
    #获取文章id
    pid = request.GET.get('pid')
    #获取文章名
    name = models.story.objects.filter(id=pid).values('sto_name','for_user__true_name').first()
    #查询文章所有章节并分配数据
    data = models.storyDetail.objects.filter(for_story__id=pid,stod_use=0).values('id','stod_title').order_by('stod_weight')
    return render(request,'story/story_index_list.html',{"data":data,"pid":pid,"name":name})

#文章首页详细页面功能
def story_index_detail(request):
    #获取文章id
    pid = request.GET.get('pid')
    #获取文章章节id
    id = request.GET.get('id')
    data = models.storyDetail.objects.filter(id=id).values('id', 'stod_title', 'stod_content').first()
    return render(request,'story/story_index_detail.html',{"data":data,"pid":pid})

#文学网后台首页
def my_story(request):
    #查询文学名称并分配变量
    data = models.story.objects.filter(for_user__id = request.session.get('user_id')).values('id','sto_name','sto_img','sto_hot','sto_use','for_kind__sto_kind','sto_intro','ctime')
    return render(request,'story/my_story.html',{'data':data})

#文学网添加界面展示
def story_add(request):
    # 获取文学分类信息，并分配数据到模板
    kind = models.stoKind.objects.values('id', 'sto_kind')
    return render(request,'story/story_add.html',{'kind':kind})

#文学网添加数据处理
def story_add_data(request):
    post = request.POST
    file = request.FILES.get('file')
    # print(post,'-----',file)
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
        if file:
            dic_data ={"sto_name": post['sto_name'], "sto_intro": post['sto_intro'], "sto_use": post['sto_use'],
                    "sto_img": upload_path}
        else:
            dic_data = {"sto_name": post['sto_name'], "sto_intro": post['sto_intro'], "sto_use": post['sto_use']}
        # 根据id修改数据
        # print(dic_data)
        models.story.objects.filter(id=id).update(**dic_data)
    else:
        # 定义写入数据库的字典
        for_kind = models.stoKind.objects.get(id =post['for_kind'])  # 外键关联不能直接写值，必须是一个外键对象
        ctime = time.strftime('%Y-%m-%d %X')  # 格式化日期时间
        dic_data = {"sto_name": post['sto_name'], "sto_intro": post['sto_intro'], "sto_use": post['sto_use'],
                    "sto_img": upload_path, "sto_hot": 1, "sto_weight": 1, "for_kind": for_kind, "ctime": ctime,"sto_sort":genRandomString()}
        print(dic_data)
        models.story.objects.create(**dic_data)
    return redirect('/my_story.html')

def story_edit(request):
    #获取要修改的id
    id = request.GET.get('id')
    # print(jmid)
    # return  HttpResponse('success')
    #过去要修改的值，并分配数据
    data = models.story.objects.filter(id = id).values().first()
    # print(data)
    return render(request,'story/story_edit.html',{'data':data})

def story_detail_list(request):
    #查询当前文章的所有章节，并分配数据
    id = request.GET.get('id')
    data_list = models.storyDetail.objects.filter(for_story__id=id).values('id', 'stod_title', 'stod_weight', 'stod_use',
                                                                      'ctime').order_by('stod_weight')
    # 分页
    from picture import pager
    current_page = request.GET.get('p', 1)
    pager = pager.Pagination('story_detail_list.html', len(data_list), current_page, 50,id=id)
    data = data_list[pager.start():pager.end()]
    #文章名称
    name = models.story.objects.filter(id = id).values('sto_name').first()
    return render(request,'story/story_detail_list.html',{"data":data,'pid':id,"name":name,'pager':pager})

#文章详情添加
def story_detail_add(request):
    #获取文章的id
    pid = request.GET.get('pid')
    return render(request,'story/story_detail_add.html',{"pid":pid})

#文章章节数据添加入库
def story_detail_add_data(request):
    pid = request.GET.get('pid')
    post = request.POST
    id = request.GET.get('id',0)
    edit = request.GET.get('edit', 0)
    # 组装排序字段
    sort = models.story.objects.filter(id=pid).values('sto_sort').first()['sto_sort']
    stod_sort = sort + post['stod_sort']
    if edit:
        # 组装字典
        dic_data = {"stod_title": post['stod_title'], "stod_use": post['stod_use'], "stod_content": post['stod_intro'],
                     "stod_weight": stod_sort}
        models.storyDetail.objects.filter(id=id).update(**dic_data)
    else:
        # print(pid,'---',post)
        # print(stod_sort)
        # return HttpResponse('test')
        for_story = models.story.objects.get(id=pid)#外键对象
        ctime = time.strftime('%Y-%m-%d %X')  # 格式化日期时间
        #组装字典
        dic_data = {"stod_title":post['stod_title'],"stod_use":post['stod_use'],"stod_content":post['stod_intro'],"for_story":for_story,"ctime":ctime,"stod_weight":stod_sort}
        # print(dic_data)
        models.storyDetail.objects.create(**dic_data)
    return redirect('/story_detail_list.html?id='+pid)

#文章章节编辑界面展示
def story_detail_edit(request):
    #获取要编辑的信息
    id = request.GET.get('id')
    pid = request.GET.get('pid')
    data = models.storyDetail.objects.filter(id = id).values().first()
    # print(data)
    return  render(request,'story/story_detail_edit.html',{"data":data,"id":id,"pid":pid})

#文章详情删除功能
def story_detail_del(request):
    #获取id作为删除的指标
    id = request.GET.get('id')
    #获取pid作为跳转传递的产数
    pid = request.GET.get('pid')
    #删除文章章节
    models.storyDetail.objects.filter(id=id).delete()
    return redirect('/story_detail_list.html?id='+pid)

#文章删除功能
def story_del(request):
    #获取要删除的文章
    id = request.GET.get('id')
    # print(id)
    # return HttpResponse(id)
    #首先删除此文章的章节
    models.storyDetail.objects.filter(for_story__id=id).delete()
    #再删除文章
    models.story.objects.filter(id=id).delete()
    #跳转到文学网后台管理页面
    return redirect('/my_story.html')