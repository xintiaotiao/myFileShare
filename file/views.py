from django.shortcuts import render,HttpResponse,redirect
from file import models
from django.db.models import Q,F
import json,pickle,os,time,random,xlwt
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#定义一个excel样式
def set_style(font_name, font_height, bold=False):
    style = xlwt.XFStyle()

    font = xlwt.Font()
    font.name = font_name  # 'Times New Roman'
    font.height = font_height
    font.bold = bold
    font.colour_index = 4

    borders = xlwt.Borders()
    borders.left = 6
    borders.right = 6
    borders.top = 6
    borders.bottom = 6

    style.font = font
    style.borders = borders
    return style

def index(request):
    #定义分页数据，实现分页效果
    # data_list = []
    # for i in range(1,100):
    #     temp={'a' : 'id'+str(i) , 'b':'Name' +str(i) , 'c':'class' +str(i)}
    #     data_list.append(temp)
    # print(data)
    #从数据库中读取数据作为数据源
    from file import pager
    current_page = request.GET.get('p',1)
    k = int(request.GET.get('k',0))
    q = request.GET.get('q','')
    # print(q)
    ex = request.GET.get('ex',0)
    if q:
        if k:
            data_list = models.File.objects.filter(Q(file_name__iregex=q)&Q(file_kind =k)).values('id', 'file_name', 'file_path',
                                                            'file_size', 'file_ip','file_intro',
                                                            'file_hot', 'file_time',
                                                            'file_kind__name').order_by("-file_time","-file_hot")
        else:
            data_list = models.File.objects.filter(Q(file_name__iregex=q)).values('id', 'file_name','file_intro',
                                                                                                   'file_path',
                                                                                                   'file_size',
                                                                                                   'file_ip',
                                                                                                   'file_hot',
                                                                                                   'file_time',
                                                                                                   'file_kind__name').order_by("-file_time","-file_hot")
    else:
        if k:
            data_list = models.File.objects.filter(Q(file_kind = k)).values('id', 'file_name','file_intro', 'file_path',
                                                                          'file_size', 'file_ip',
                                                                          'file_hot', 'file_time',
                                                                          'file_kind__name').order_by("-file_time","-file_hot")
        else:
            data_list = models.File.objects.values('id', 'file_name', 'file_path','file_intro',
                                                                          'file_size', 'file_ip',
                                                                          'file_hot', 'file_time',
                                                                          'file_kind__name').order_by("-file_time","-file_hot")

    #这里添加代码用来导出查询的数据到excel表中
    # print(data_list,len(data_list))
    if ex:
        excel = xlwt.Workbook()
        sheet = excel.add_sheet(time.strftime('%Y-%m-%d'))
        head_list = ['id', '文件名','存放路径', '文件介绍','文件大小', '上传者','点击量', '上传时间', '所属类别']
        for i in range(len(head_list)):
            sheet.write(0, i, head_list[i], set_style("Times New Roman", 220))
        for i in range(1,len(data_list)):
            sheet.write(i,0,data_list[i-1]['id'])
            sheet.write(i, 1, data_list[i-1]['file_name'])
            sheet.write(i, 3, data_list[i-1]['file_intro'])
            sheet.write(i, 2, data_list[i-1]['file_path'])
            sheet.write(i, 4, data_list[i-1]['file_size'])
            sheet.write(i, 5, data_list[i-1]['file_ip'])
            sheet.write(i, 6, data_list[i-1]['file_hot'])
            sheet.write(i, 7,str(data_list[i-1]['file_time']))
            sheet.write(i, 8, data_list[i-1]['file_kind__name'])
        try:
            excel.save('C:/Users/Administrator/Desktop/'+'文件信息表_'+str(random.randrange(100,999))+'.xls')
        except Exception as e:
            return HttpResponse(e)
        finally:
            return  HttpResponse('导出文件成功！')

        # excel.save
    pager = pager.Pagination('index.html',len(data_list),current_page,q,k,10)
    data = data_list[pager.start():pager.end()]
    kind = models.Kind.objects.values('id','name').order_by('id')
    # data1= pickle.dumps(data)
    # print(pickle.loads(data1))
    # return HttpResponse(data1)
    return render(request,'file/index.html',{'data':data,'kind':kind,'pager':pager,'q':q,'k':k})

from django.http import FileResponse
def read_file(fn,chunk_size=1024):
    while True:
        c = fn.read(chunk_size)
        if c:
            yield
        else:
            break
def download(request):
    from urllib.parse import unquote, quote
    did = request.GET.get('id')
    models.File.objects.filter(id = did).update(file_hot = F('file_hot')+1)
    file_info = models.File.objects.filter(id = did).values('file_name','file_path').first()
    # print(file_info)
    file_path = BASE_DIR+'/'+file_info['file_path']
    # 首先判断要删除的文件是否存在，存在则删除
    if os.path.exists(file_path):
        file_name_list = file_path.split('.')
        file_name = file_info['file_name']+'.'+file_name_list[len(file_name_list)-1]
        def file_iterator(fn, chunk_size=1024*20):
            while True:
                c = fn.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        fn = open(file_path, 'rb')
        response = FileResponse(file_iterator(fn))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file_name)
        return response
    else:
        return HttpResponse('该原文件已损坏或无效，请删除！')



def upload(request):
    try:
        if request.method == "POST":
            post = request.POST
            file_obj = request.FILES.get('file')
            # size = len(file_obj.read())/1024/1024
            file_size = round(len(file_obj.read())/1024/1024,2)#file_obj.read()只能读取一次，下面再用到就会读取为空
            if file_size > 1024 :
                return HttpResponse('单文件上传最大1G...')
            # print(post)
            # print(file_obj)
            if not os.path.isdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d')):
                os.mkdir(BASE_DIR + '/static/upload/' + time.strftime('%Y-%m-%d'))
            upload_path = 'static/upload/' + time.strftime('%Y-%m-%d') + '/' + str(
                random.randrange(100, 999)) + '_' + file_obj.name
            f = open(upload_path, 'wb')
            # file_size = str(round(len(file_obj.read())/1024/1024,2)) +'M'
            file_ip = request.META['REMOTE_ADDR']
            # f = open('%Y-%m-%d.jpg','wb')
            for chunks in file_obj.chunks(1024):
                f.write(chunks)
            f.close()

            #这里是处理提交过来的数据并写入数据库
            file_dic = {"file_kind_id": post['file_kind'], "file_intro": post['file_intro'],
                        "file_name": post['file_name'], "file_size": file_size, "file_ip": file_ip ,
                        "file_path":upload_path,"file_hot":1,"file_time":time.strftime('%Y-%m-%d %X')
                        }
            # print(file_dic)
            # res= models.File.objects.create(file_kind= post['file_kind'], file_intro=post['file_intro'],file_name=post['file_name'],file_size=file_size,file_ip=file_ip)
            res = models.File.objects.create(**file_dic)
            # print(res)
            return HttpResponse('success')
    except Exception as e:
        HttpResponse('上传失败，错误原因：'+str(e))
    # finally:
    #     return HttpResponse("success")

def file_del(request):
    try:
        # 根据传递的id查询要修改图集的信息
        id = request.GET.get('id')
        # 首先判断要删除的文件是否存在，存在则删除
        dic = models.File.objects.filter(id=id).values('file_path').first()
        # print(dic)
        if os.path.exists(BASE_DIR + '/' + dic['file_path']):
            os.remove(BASE_DIR + '/' + dic['file_path'])
        models.File.objects.filter(id=id).delete()
        return HttpResponse('success')
    except Exception as e:
       return HttpResponse(str(e))

#网络爬虫测试，自动登录、自动评论功能实现
def pachong(request):
    return render(request,"file/pachong.html")


import requests, random
ses = requests.Session()
def py_requests(request):
    if not request.session['user_id']:

        ### 1、首先登陆任何页面，获取cookie
        response1 = ses.get(url="http://10.172.196.127/pic_index.html")
        # print(i1.cookies)
        ## 2、用户登陆，携带上一次的cookie，后台对cookie中的 gpsd 进行授权
        response2 = ses.get(
            url="http://10.172.196.127/login.html",
            #get方式的参数不能用data或json，params返回的是字节类型，如果有汉字需要转码
            params={
                'username2': "otis",
                'password2': "123456"
            },
            # cookies=i1.cookies
        )
        # print(response2.text, response2.headers)
    ##登录后进行评论,并且点击量自动增加，可以用来刷取点击量
    response3 = ses.get(
        url="http://10.172.196.127/pic_hot_add.html?pid=6",
        # params={
        #     "pid": 6,
        #     'content': "python_" + str(random.randrange(100,999,2))
        # }
    )
    return HttpResponse("success")

#配置404页面
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

# from django.conf.urls import handler404, handler500
# handler404 = views.page_not_found
# handler500 = views.page_error

@csrf_exempt
def page_not_found(request):
    return render_to_response('file/404.html')

@csrf_exempt
def page_error(request):
    return render_to_response('file/500.html')


