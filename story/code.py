


#生成随机字符串
import random,string
def genRandomString(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))