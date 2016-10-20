#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.shortcuts import get_list_or_404,get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import StringIO
import sys
import requests
import urllib
from django.contrib import auth
import wxconfig as wxconfig
import random
# Create your views here.

#提交订单
@login_required
@csrf_exempt
def submitorder(request,type):
    if request.method == "POST":
        #预约
        if type == str(0):
            try:
                productpk = request.POST.get('productpk',None)
                personpk = request.POST.get('personpk',None)
                time = request.POST.get('time',None)
                product = get_object_or_404(Product,pk=productpk)
                person = get_object_or_404(Person,pk=personpk)
                dattime =  timezone.datetime.strptime(time, "%Y-%m-%d %H:%M")
                if dattime<timezone.now():
                    return HttpResponse("请正确选择时间",status=400)
                try:
                    order = ApointmentOrder.objects.get(product=product,person=person,user=request.user,ordertime=time)
                except ApointmentOrder.DoesNotExist:
                    order = ApointmentOrder(product=product, person=person, user=request.user, ordertime=time)
                    order.save()
                    return HttpResponse('预约成功')
                else:
                    return HttpResponse('您已预约了该项目')
            except Exception:
                return HttpResponse(Exception.message, status=400)
    return HttpResponse(status=200)


# 按项目预约
@login_required
def queuemain(request,productPk):
    product = get_object_or_404(Product,pk=productPk)
    persons = get_list_or_404(Person,product = product)
    return render(request,'queuemain.html',locals())

# 预约人
@login_required
def queueperson(request,productPk,personPk):
    now = timezone.now().strftime("%Y-%m-%dT%H:%M")
    product = get_object_or_404(Product, pk=productPk)
    person = get_object_or_404(Person,pk=personPk)
    return render(request,'queueoperson.html',locals())


#我的预约/排队
@login_required
@csrf_exempt
def myorder(request,type):
    #预约
    if type == str(0):
        try:
            appointments = ApointmentOrder.objects.filter(user=request.user)  # get_list_or_404(ApointmentOrder,user=request.user)
        except ApointmentOrder.DoesNotExist:
            pass
        return render(request,'myappointment.html',locals())
    #排队
    elif type == str(1):
        if request.method == "POST":
            try:
                queuenumbers = Queuenumber.objects.all()
                if not queuenumbers:
                    return HttpResponse('暂停排队了.')
                queuenumber = queuenumbers[0]
                if queuenumber.isacceivequeue == False:
                    return HttpResponse('暂停排队..')
                queueorders = QueueOrder.objects.filter(user=request.user)
                if queueorders:
                    queueorder = queueorders[0]
                    if queueorder.create_time < queuenumber.create_time or queueorder.number < queuenumber.currentnumber:
                        raise QueueOrder.DoesNotExist
                else:
                    raise QueueOrder.DoesNotExist
            except QueueOrder.DoesNotExist:
                queueorder = QueueOrder(user=request.user, number=queuenumber.lastqueuenumber + 1)
                queueorder.save()
                queuenumber.lastqueuenumber = queuenumber.lastqueuenumber + 1;
                queuenumber.save()
            else:
                pass
            return HttpResponse("排队成功")
        elif request.method == 'GET':
            try:
                queuenumbers = Queuenumber.objects.all()
                if not queuenumbers:
                    return render(request, 'myqueue.html', locals())
                queuenumber = queuenumbers[0]
                if queuenumber.isacceivequeue == False:
                    return render(request, 'myqueue.html', locals())
                queueorders = QueueOrder.objects.filter(user=request.user)
                if queueorders:
                    queueorder = queueorders[0]
                    if queueorder.create_time < queuenumber.create_time or queueorder.number < queuenumber.currentnumber:
                        raise QueueOrder.DoesNotExist
                else:
                    raise QueueOrder.DoesNotExist
            except QueueOrder.DoesNotExist:
                queueorder = None
                return render(request,'myqueue.html',locals())
            else:
               if queueorder:
                   personnumber = queueorder.number - queuenumber.currentnumber
                   times = personnumber * 10
            return render(request,'myqueue.html',locals())

def syncdb(request,arg):
    #重定向标准输出重定向到内存的字符串缓冲(由StringIO模块提供)
    saveout = sys.stdout
    log_out = StringIO.StringIO()
    sys.stdout = log_out
    #利用django提供的命令行工具来执行“manage.py syncdb”
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", arg, "--noinput"])
    #获得“manage.py syncdb”的执行输出结果，并展示在页面
    result = log_out.getvalue()
    sys.stdout = saveout
    return HttpResponse(result.replace("\n","<br/>"))

#引导用户微信网页授权
def wechatscope(request):
    backurl = request.GET.get('next',None)
    redirecturl = wxconfig.redirecturl
    if backurl is not None:
        encodeurl = urllib.quote(redirecturl+'?next='+backurl)
    else:
        encodeurl = urllib.quote(redirecturl)
    print  encodeurl
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=123#wechat_redirect" %(wxconfig.appID,encodeurl)
    return HttpResponseRedirect(url)



class Accesstoken(object):

    @classmethod
    def deletetoken(cls):
        access_token = Access_token.objects.get(pk=1)
        access_token.delete()


    @classmethod
    def getToken(cls):

        def getTokenFromWX():
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                wxconfig.appID, wxconfig.appsecret)
            res = requests.get(url)
            try:
                dic = res.json()
                token = dic['access_token']
            except Exception:
                return False
            else:
                access_token = Access_token(token=token)
                access_token.save()
                return access_token.token

        try:
            access_token = Access_token.objects.get(pk=1)
        except Access_token.DoesNotExist:
            # 不存在就去获取
            wxtoken = getTokenFromWX()
            return wxtoken
        else:
            # 判断是否过期
            now = timezone.now()
            timedelta = now - access_token.time
            if timedelta < timezone.timedelta(seconds=7000):
                print "数据库token"
                return access_token.token
            else:
                wxtoken = getTokenFromWX()
                return wxtoken


#网页授权返回code ->获取用户信息 ->设置成登陆状态
def redirect(request):
    backurl = request.GET.get('next',None)
    code = request.GET.get('code')
    # state = request.GET.get('state')
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" %(wxconfig.appID,wxconfig.appsecret,code)
    res = requests.get(url)
    try:
       dic = res.json()
       opendid = dic['openid']
    except Exception:
        return HttpResponse('openid json error')
    else:
        #获取access_token
        token = Accesstoken.getToken()
        if not token:
            return HttpResponse('token error')
        #获取用户信息
        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" %(token,opendid)
        res = requests.get(url)
        try:
            dic = res.json()
            try:
                expired = dic['errcode']
                print expired
            except Exception:
                pass
            else:
                Accesstoken.deletetoken()
                token = Accesstoken.getToken()
                url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (
                    token, opendid)
                print url
                res = requests.get(url)
                dic = res.json()
        except Exception:
            return HttpResponse('json erron')
        else:
            try:
                jsubscribe = dic['subscribe']
                jopenid = dic['openid']
                jnickname = dic['nickname']
                jsex = int(dic['sex'])
                jheadimgurl = dic['headimgurl']
            except KeyError:
                print KeyError
            try:
                cUser = CustomUser.objects.get(openid = jopenid)
            except CustomUser.DoesNotExist:
                cUser = CustomUser(openid = jopenid,nickname=jnickname,sex=jsex,headimgurl=jheadimgurl)
                a = str(random.randint(1,10000))
                user = User.objects.create_user(username=jnickname+a,password=jopenid,email="")
                user.save()
                cUser.user = user
                cUser.save()
                #去设置成登陆状态
                user = auth.authenticate(username=user.username, password=cUser.openid)#authenticate密码需要的是没加密的密码
                if user is not None:
                    auth.login(request, user)
                else:
                    return HttpResponse('login error')
            else:
                #去设置成登陆状态
                print 'user had'
                user = auth.authenticate(username=cUser.user.username, password=cUser.openid)
                if user is not None:
                    auth.login(request, user)
                else:
                    return HttpResponse('login error')
            if backurl is not None:
                return HttpResponseRedirect(backurl)
            else:
                return HttpResponseRedirect('/queue/myorder/1')



