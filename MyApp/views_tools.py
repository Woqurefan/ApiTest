from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from MyApp.models import *
import json
import requests
from allpairspy import AllPairs
import xlrd
import xlwt
import os

# 获取公共参数
def glodict(request):
    userimg = str(request.user.id)+'.png'  #这里我们写死png后缀，因为上传时候我们也可以强行弄成这个png后缀。
    res = {"username":request.user.username,"userimg":userimg}
    return res


# 进入正交工具页面
def zhengjiao(request):
    return render(request,'welcome.html',{"whichHTML": "zhengjiao.html","oid":request.user.id,**glodict(request) })

# 正交工具运行
def zhengjiao_play(request):
    end_values = request.GET['end_values'].split(',')

    filter_input = request.GET['filter_input'] #提取出过滤规则
    filter_input = filter_input.replace('，',',').replace(' ','').replace('\n','') #进行修正

    new_values = [ i.split('/') for i in end_values ]
    res = []
    filter = []
    for i in AllPairs(new_values):
        # 判断是否中了过滤规则
        for f in filter_input.split(','):#遍历过滤规则
            left = f.split('-')[0]
            try:
                right = f.split('-')[1]
            except:
                res.append(i)
                break
            if left in i and right in i:
                filter.append({"case":i,"filter":[left,right]})
                break
        else:
            res.append(i)
    # print('res:',res)
    # print('filter:',filter)

    wugu = [] #声明无辜组合列表
    #开始对filter，整理出无辜组合
    for d in filter: #d此时是个字典
        case = d['case']
        f_case = d['filter']
        cha = list(set(case).difference(set(f_case))) #求出剩余的其他子状态的列表
        for f_c in f_case: # 遍历f_case，拆开中规则的俩个子状态，分别和其他子状态 组合成新的列表，视为无辜组合
            tmp = cha+[f_c]
            wugu.append(tmp)

    # print('wugo: ',wugu)
    bdgl = []
    for w in wugu:
        # 看看无辜组合是否已经存在于res中
        for i in res:
            if set(w).issubset(set(i)) : #判断w是否是i的子列表
                break
        else: #只有当正常结束才会运行,正常结束代表未存在res，可以继续往后走。
            # 用一个新的非中过滤规则的子状态填充，形成完整的组合
            # print('-----------------')
            # print(w) #此时的w 是要添加新的子状态 组成完整组合的～
            which = [v for v in new_values if set(v).intersection(set(w)) == set()][0]  # 用交集函数 确认那个需要增加的输入条件：
            # print(which)
            for whi in which:
                new_zuhe = w + [whi] #变成新组合
                # print('新组合:',new_zuhe)
                # 判断是否中了过滤规则
                for f in filter_input.split(','):  # 遍历过滤规则
                    left = f.split('-')[0]
                    right = f.split('-')[1]
                    if left in new_zuhe and right in new_zuhe: #说明中标
                        # print('中了，则该组合不行，看下一个组合吧～')
                        break
                else: #说明新组合没中过滤
                    # print('全程没中过滤，很nice')
                    # 对有效新组合 进行 顺序校验！
                    # print('--------')
                    # print(new_zuhe)
                    # print(new_values)
                    new_tmp = [list(set(nv).intersection(set(new_zuhe)))[0] for nv in new_values if set(nv).intersection(set(new_zuhe))]
                    # print(new_tmp)
                    # 校验后，再添加给res
                    res.append(new_tmp) #
                    break
                # 中了过滤 走这里,所以要换下一个新组合
                continue
            else: # 说明是没有break出来的，被动过滤组合，给bdgl组合列表送去把
                bdgl.append('-'.join(w))
            # break出来的，说明找到了有效组合，所以这个无辜组合已经可以了，赶紧搞下一个无辜组合把～

    d = { "res" : res,"bdgl":bdgl}
    return HttpResponse(json.dumps(d),content_type="application/json")

# 正交工具导出
def zhengjiao_excel(request):
    end_keys = request.GET['end_keys'].split(',')
    end_values = request.GET['end_values'].split(',')
    new_values = [i.split('/') for i in end_values]
    res = []
    for i in AllPairs(new_values):
        res.append(i)
    # 先创建
    wqrf_book = xlwt.Workbook(encoding='utf-8') # 创建excel
    wqrf_sheet = wqrf_book.add_sheet("正交结果") # 创建sheet页
    for i in range(len(res)):
        case_index = '用例:'+str(i+1) # 用例序号
        hb = list(zip(end_keys,res[i])) #把key和value进行合并
        wqrf_sheet.write(i,0,case_index)  # 写入，i为行，0为第一例

        case = [':'.join(list(i)) for i in hb] #进行格式化，便于阅读
        for c in range(len(case)):
            wqrf_sheet.write(i,1+c , case[c])  # 写入，i为行，1为第二例


    wqrf_book.save('MyApp/static/tmp_zhengjiao.xls') #保存

    return HttpResponse('')
