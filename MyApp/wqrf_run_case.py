# -*- coding:utf-8 -*-
import sys,os,django
path = "../ApiTest"
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApiTest.settings")
django.setup()
from MyApp.models import *
from MyApp.views import global_datas_replace,encyption
import re
import json
import requests

def do_step(step_id,tmp_datas):
    '请求数据准备'
    ## 计算项目id
    project_id = DB_cases.objects.filter(id=DB_step.objects.filter(id=step_id)[0].Case_id)[0].project_id
    # 拿到step
    step = DB_step.objects.filter(id=step_id)[0]
    # 初始化请求方式
    api_method = step.api_method
    # 初始化url
    api_url = step.api_url
    # url添加全局变量
    api_url = global_datas_replace(project_id, api_url)
    ## 取出证书开关
    api_cert = step.cert
    ## 域名初始化
    api_host = step.api_host
    ## 域名添加全局变量
    api_host = global_datas_replace(project_id, api_host)
    ## 请求体初始化
    api_body = step.api_body
    ## 请求方式初始化
    api_method = step.api_method
    ## 请求体添加全局变量
    api_body = global_datas_replace(project_id, api_body)
    ## 返回值处理方式初始化
    get_path = step.get_path
    get_zz = step.get_zz
    assert_zz = step.assert_zz
    assert_qz = step.assert_qz
    assert_path = step.assert_path
    ## 请求头初始化
    api_header = step.api_header
    ## 请求头添加全局变量
    api_header = global_datas_replace(project_id, api_header)
    ## 公共请求头获取
    ts_project_headers = step.public_header.split(',')  # 获取公共请求头
    ## 请求体类型初始化：
    api_body_method = step.api_body_method
    ## Mock返回值初始化
    mock_res = step.mock_res
    ## 是否mock判断
    if mock_res not in ['', None, 'None']:
        res = mock_res
    ## 请求头为空处理
    if api_header == '':
        api_header = '{}'

    ## 占位符变量替换
    # url 处理
    rlist_url = re.findall(r"##(.*?)##", api_url)
    for i in rlist_url:
        api_url = api_url.replace("##" + i + "##", tmp_datas[i])

    # header 处理
    rlist_header = re.findall(r"##(.*?)##", api_header)
    for i in rlist_header:
        api_header = api_header.replace("##" + i + "##", repr(tmp_datas[i]))
    # 请求体 处理
    if api_body_method == 'none':
        pass
    elif api_body_method == 'form-data' or api_body_method == 'x-www-form-urlencoded':
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", str(eval(i)))

    elif api_body_method == 'Json':
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##", repr(tmp_datas[i]))

    else:
        rlist_body = re.findall(r"##(.*?)##", api_body)
        for i in rlist_body:
            api_body = api_body.replace("##" + i + "##",  tmp_datas[i])

    ## 域名额外处理-全局域名
    if api_host[:4] == '全局域名':
        project_host_id = api_host.split('-')[1]
        api_host = DB_project_host.objects.filter(id=project_host_id)[0].host

    ## header转换为字典
    try:
        header = json.loads(api_header)  # 处理header
    except:
        header = eval(api_header)
    # 在这遍历公共请求头，并把其加入到header的字典中。
    for i in ts_project_headers:
        if i == '':
            continue
        project_header = DB_project_header.objects.filter(id=i)[0]
        header[project_header.key] = project_header.value
    ## 最终url生成
    if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
        url = api_host[:-1] + api_url
    elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有/
        url = api_host + '/' + api_url
    else:  # 肯定有一个有/
        url = api_host + api_url
    ## 登录态融合
    api_login = step.api_login  # 获取登陆开关
    if api_login == 'no':
        login_res = {}

    else :  # 需要登录态
        Case_id = step.Case_id  # 先求出当前执行step所属的case_id
        global login_res_list  # 新建一个登陆态列表
        try:
            eval('login_res_list')
        except:
            login_res_list = []  # 判断是否存在，若不存在，则创建空的。
        # 去login_res_list中查找是否已经存在
        for i in login_res_list:
            if i['Case_id'] == Case_id:  # 说明找到了.直接用。
                print('找到了')
                login_res = i
                break
        else:  # 说明没找到，要创建
            print('没找到要创建')
            from MyApp.views import project_login_send_for_other
            login_res = project_login_send_for_other(project_id) # 调用我们之前写好的获取函数
            login_res['Case_id'] = Case_id  # 给它加入 大用例id 标记
            login_res_list.append(login_res)
        # 运行到这的时候，可以肯定已经有了这个login res了
        ## url插入
        if '?' not in url:
            url += '?'
            if type(login_res) == dict:
                for i in login_res.keys():
                    url += i + '=' + login_res[i] + '&'
        else:  # 证明已经有参数了
            if type(login_res) == dict:
                for i in login_res.keys():
                    url += '&' + i + '=' + login_res[i]
        ## header插入
        if type(login_res) == dict:
            header.update(login_res)

    ## 加密策略
    step_encyption = step.sign
    if step_encyption == 'yes':
        url, api_body = encyption(url, api_body_method, api_body, project_id)

    ## 证书融合
    if api_cert == 'yes':
        cert_name = 'MyApp/static/Certs/%s' % DB_project.objects.filter(id=project_id)[0].cert
    else:
        cert_name = ''

    ## 数据库写入请求数据
    r_step = DB_wqrf_step_report.objects.get_or_create(id=step_id)[0]
    r_step.request_data = json.dumps({
        "url":url,
        "method":api_method,
        "api_body":api_body,
        "api_body_method":api_body_method
    })

    '执行请求'
    ## none请求
    if api_body_method == 'none' or api_body_method == 'null':
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data={}, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data={}, cert=cert_name)

    ## form-data请求
    elif api_body_method == 'form-data':
        files = []
        payload = ()
        for i in eval(api_body):
            payload += ((i[0], i[1]),)

        if type(login_res) == dict:
            for i in login_res.keys():
                payload += ((i, login_res[i]),)

            response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files,
                                        cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, files=files,
                                         cert=cert_name)

    ## x-www-form-urlencoded请求
    elif api_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'

        payload = ()
        for i in eval(api_body):
            payload += ((i[0], i[1]),)

        if type(login_res) == dict:
            for i in login_res.keys():
                payload += ((i, login_res[i]),)

        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)

    ## GraphQL请求
    elif api_body_method == 'GraphQL':
        header['Content-Type'] = 'application/json'
        query = api_body.split('*WQRF*')[0]
        graphql = api_body.split('*WQRF*')[1]
        try:
            eval(graphql)
        except:
            graphql = '{}'
        payload = '{"query":"%s","variables":%s}' % (query, graphql)
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=payload, cert=cert_name)

    ## raw的五种请求
    else:  # 这时肯定是raw的五个子选项：
        if api_body_method == 'Text':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Json':
            api_body = json.loads(api_body)
            for i in login_res.keys():
                api_body[i] = login_res[i]
            api_body = json.dumps(api_body)
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Html':
            header['Content-Type'] = 'text/plain'

        if api_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        if type(login_res) == dict:
            response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'),
                                        cert=cert_name)
        else:
            response = login_res.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'),
                                         cert=cert_name)
    response.encoding = "utf-8"
    res = response.text #最终结果文案

    # 返回结果存入数据库表
    r_step.response = res

    '结果处理'
    # 新建临时变量列表
    tmp_d = {}
    ## 对返回值res提取-路径法
    if get_path != '':  # 说明有设置
        for i in get_path.split('\n'):
            key = i.split('=')[0].rstrip()
            path = i.split('=')[1].lstrip()
            py_path = ""
            for j in path.split('/'):
                if j != '':
                    if j[0] != '[':
                        py_path += '["%s"]' % j
                    else:
                        py_path += j
            value = eval("%s%s" % (json.loads(res), py_path))
            tmp_d[key] = value
    ## 对返回值res提取-正则法
    if get_zz != '':  # 说明有设置
        for i in get_zz.split('\n'):
            key = i.split('=')[0].rstrip()
            zz = i.split('=')[1].lstrip()
            value = re.findall(zz, res)[0]
            tmp_d[key] = value

    ## 对返回值断言-路径法

    tmp_assert_result = {} #先弄个总的字典存放
    if assert_path != '':  # 说明有设置
        for i in assert_path.split('\n'):
            path = i.split('=')[0].rstrip()
            want = eval(i.split('=')[1].lstrip())
            py_path = ""
            for j in path.split('/'):
                if j != '':
                    if j[0] != '[':
                        py_path += '["%s"]' % j
                    else:
                        py_path += j
            value = eval("%s%s" % (json.loads(res), py_path))
            tmp_assert_result[i] = ( want==value )

    ## 对返回值断言-正则
    if assert_zz != '':
        for i in assert_zz.split('\n'):
            zz = i.split('=')[0].rstrip()
            want = i.split('=')[1].lstrip()
            value = re.findall(zz, res)[0]
            tmp_assert_result[i] = ( want==value )


    ## 对返回值断言-全值检测
    if assert_qz != '':
        for i in assert_qz.split('\n'):
            if i not in res:
                tmp_assert_result[i] = (False)
            else:
                tmp_assert_result[i] = (True)

    r_step.assert_result = json.dumps(tmp_assert_result)
    r_step.step_id = step_id
    r_step.save()
    return tmp_d

def main_request(case_id):
    '入口主函数'
    tmp_datas = {} # 总临时变量列表
    steps = DB_step.objects.filter(Case_id=case_id)
    for i in steps:
        tmp_d = do_step(i.id,tmp_datas) #tmp_d为单步骤临时变量，列表
        tmp_datas.update(tmp_d)


