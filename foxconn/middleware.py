from django.utils.deprecation import MiddlewareMixin
import re

#对登录路由进行限制的中间件
class AuthMD(MiddlewareMixin):
    white_list = ['/','/pic_index.html','/register.html','/check_user.html','/login.html','/pic_index_new.html','/pic_hot_add.html',\
                  '/story_index.html','/sto_hot_add.html','/story_index_detail.html','/story_index_list.html','/index.html',\
                  '/download.html','/upload.html','/file_del.html']  # 白名单
    black_list = [ ]  # 黑名单

    def process_request(self, request):
        from django.shortcuts import redirect,HttpResponse
        next_url = request.path_info
        # print(re.match('/admin', next_url))
        # print(next_url)
        if next_url in self.white_list:#未做限定的直接访问
            pass
        elif  request.session.get("user_id"):  #不在白名单中的所有路由，session 中user_id为空，则跳到登录
            pass
        elif re.match('/admin', next_url):
            pass
        else:
            return HttpResponse('您还未登录，请先登录后访问！')

        #这里还可以编写RBAC权限控制代码
