# """
# 1、采用requests和beautyful模块演示爬虫操作
# 2、自动登录人员管控系统
# 3、抓取人员管控系统中的门岗信息并保存为字典格式
# 4、链接mysql数据库并把抓取的数据保存入数据库中
# 5、将数据库中的数据展示在页面上
# """
#
# import requests
# from bs4 import BeautifulSoup
#
# #首次登录，获取cookie值及需要提交的数据
# ret1 = requests.get(
#     url = "http://guard.gl.idpbg.efoxconn.com/Login.aspx"
# )
# login_cookie = ret1.cookies.get_dict()
# login_text = ret1.text
# # print(login_text)
# soup = BeautifulSoup(login_text,features="lxml")
# __VIEWSTATE = soup.find(name='input',id='__VIEWSTATE').attrs['value']
# __EVENTVALIDATION = soup.find(name='input',id='__EVENTVALIDATION').attrs['value']
# __VIEWSTATEGENERATOR = soup.find(name='input',id='__VIEWSTATEGENERATOR').attrs['value']
# # print(__VIEWSTATE,__EVENTVALIDATION,__VIEWSTATEGENERATOR)
#
# #第二次登录，将上次访问的cookie和从页面提取的表单数据发送过去
# """
# __EVENTTARGET: btnSubmit
# __EVENTARGUMENT:
# __VIEWSTATE: /wEPDwUKLTIzMDYwNTI5OWRkUPxK+E4R+6LuZOHWzJsxcHBlhys=
# __EVENTVALIDATION: /wEWBQKjtvnTDgKl1bKzCQK1qbSRCwLCi9reAwKgt7D9CmZF+Y9LhOA275EeMzIpmYDI4Unr
# txtUserName: G4869784
# txtPassword: IDPBG0..
# """
# ret2 = requests.post(
#     url = "http://guard.gl.idpbg.efoxconn.com/Login.aspx",
#     data = {
#         "__EVENTTARGET":"btnSubmit",
#         "__EVENTARGUMENT":"",
#         "__VIEWSTATE":__VIEWSTATE,
#         "__EVENTVALIDATION":__EVENTVALIDATION,
#         "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
#         "txtUserName":"G4869784",
#         "txtPassword":"IDPBG0.."
#     },
#     cookies = login_cookie,
#     headers = {
#         "Origin":"http://guard.gl.idpbg.efoxconn.com",
#         "Referer" :"http://guard.gl.idpbg.efoxconn.com/Login.aspx",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"   }
# )
# # print(ret2.request.headers)
#
# #第三次登录，带着第一次登录的coolies，获取门岗信息
# ret3 = requests.get(
#     url = "http://guard.gl.idpbg.efoxconn.com/ECSPage/GuardPage/BS_GuardBasicInfo.aspx?id=D87F934FC8156F51E043876FAC0A272F",
#     cookies = login_cookie
# )
# print(ret3.text)

"""
演示安全时空网
"""
# num_list = []
# for i in range(1,50):
#     num_list.append(i)
# # print(num_list.__iter__())
# for item in num_list:
#     try:
#         res = requests.get(
#             url = "http://10.172.196.127/download.html?id=%s" %(item),
#             stream = True
#         )
#     except Exception as e:
#         print(e)
#     finally:
#         if res:
#             with open("test/"+str(item),"wb") as f:
#                 for chunk in res.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()

