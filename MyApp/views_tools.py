from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *
import json
import requests


# 获取公共参数
def glodict(request):
    userimg = str(request.user.id)+'.png'  #这里我们写死png后缀，因为上传时候我们也可以强行弄成这个png后缀。
    res = {"username":request.user.username,"userimg":userimg}
    return res


# 进入正交工具页面
def zhengjiao(request):
    return render(request,'welcome.html',{"whichHTML": "zhengjiao.html","oid":request.user.id,**glodict(request) })
