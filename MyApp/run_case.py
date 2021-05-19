# -*- coding:utf-8 -*-

import unittest,time,re,json,requests
from MyApp.A_WQRFhtmlRunner import HTMLTestRunner

import sys,os,django
path = "../ApiTest"
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApiTest.settings")
django.setup()
from MyApp.models import *
from MyApp.views import global_datas_replace

class Test(unittest.TestCase):
    '测试类'
    @classmethod
    def setUpClass(cls):
        # print('收尾功能')
        try:
            for i in login_res_list:
                if i['Case_id'] == cls.Case_id:
                    # print('进行删除中～')
                    login_res_list.remove(i)
                    break
        except:
            pass

    def demo(self,step):
        time.sleep(3)
        # 算出项目id
        project_id = DB_cases.objects.filter(id=DB_step.objects.filter(id=step.id)[0].Case_id)[0].project_id
        # 提取所有请求数据
        api_method = step.api_method
        api_url = step.api_url
        api_url = global_datas_replace(project_id,api_url)

        api_host = step.api_host
        api_host = global_datas_replace(project_id,api_host)

        api_header = step.api_header
        api_header = global_datas_replace(project_id,api_header)

        api_body_method = step.api_body_method
        api_body = step.api_body
        api_body = global_datas_replace(project_id,api_body)

        get_path = step.get_path
        get_zz = step.get_zz
        assert_zz = step.assert_zz
        assert_qz = step.assert_qz
        assert_path = step.assert_path
        mock_res = step.mock_res
        ts_project_headers = step.public_header.split(',')  # 获取公共请求头
        if api_header == '':
            api_header = '{}'

        if mock_res not in ['',None,'None']:
            res = mock_res
        else:
            ## 检查是否需要进行替换占位符的
            rlist_url = re.findall(r"##(.*?)##",api_url)
            for i in rlist_url:
                api_url = api_url.replace("##"+i+"##",str(eval(i)))


            rlist_header = re.findall(r"##(.*?)##",api_header)
            for i in rlist_header:
                api_header = api_header.replace("##"+i+"##",repr(str(eval(i))))

            if api_body_method == 'none':
                pass
            elif api_body_method == 'form-data' or api_body_method == 'x-www-form-urlencoded':
                rlist_body = re.findall(r"##(.*?)##",api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##"+i+"##",str(eval(i)))

            elif api_body_method == 'Json':
                rlist_body = re.findall(r"##(.*?)##",api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##"+i+"##",repr(eval(i)))

            else:
                rlist_body = re.findall(r"##(.*?)##", api_body)
                for i in rlist_body:
                    api_body = api_body.replace("##" + i + "##", str(eval(i)))

            ## 实际发送请求

            # 处理host域名
            if api_host[:4] == '全局域名':
                project_host_id = api_host.split('-')[1]
                api_host = DB_project_host.objects.filter(id=project_host_id)[0].host


            # 处理header
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


            # 拼接完整url
            if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
                url = api_host[:-1] + api_url
            elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有/
                url = api_host + '/' + api_url
            else:  # 肯定有一个有/
                url = api_host + api_url

            # 登陆态代码：
            api_login = step.api_login  # 获取登陆开关
            if api_login == 'yes':  # 需要判断
                Case_id = DB_step.objects.filter(id=step.id)[0].Case_id  #先求出当前执行step所属的case_id
                global login_res_list #新建一个登陆态列表
                try:
                    eval('login_res_list')
                except:
                    login_res_list = []   #判断是否存在，若不存在，则创建空的，一般只有平台重启后才会触发一次

                # 去login_res_list中查找是否已经存在
                for i in login_res_list:
                    if i['Case_id'] == Case_id: #说明找到了.直接用。
                        print('找到了')
                        login_res = i
                        break
                else: #说明没找到，要创建
                    print('没找到要创建')
                    from MyApp.views import project_login_send_for_other
                    login_res = project_login_send_for_other(project_id)
                    login_res['Case_id'] = Case_id # 给它加入 大用例id 标记
                    login_res_list.append(login_res)

                # 运行到这的时候，可以肯定已经有了这个login res了
                print(login_res)

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
            else:
                login_res = {}

            ## 输出请求数据
            print('\n')
            print('【url】：', url)
            print('【header】：', json.dumps(header))
            print('【method】：', api_method)
            print('【body_method】：', api_body_method)
            print('【body】：', api_body)  # 目前graphQL方法的显示上仍然未优化过


            if api_body_method == 'none' or api_body_method=='null':
                if type(login_res) == dict:
                    response = requests.request(api_method.upper(), url, headers=header, data={})
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data={})


            elif api_body_method == 'form-data':
                files = []
                payload = ()
                for i in eval(api_body):
                    payload += ((i[0], i[1]),)

                if type(login_res) == dict:
                    for i in login_res.keys():
                        payload += ((i, login_res[i]),)

                    response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload, files=files)


            elif api_body_method == 'x-www-form-urlencoded':
                header['Content-Type'] = 'application/x-www-form-urlencoded'

                payload = ()
                for i in eval(api_body):
                    payload += ((i[0], i[1]),)

                if type(login_res) == dict:
                    for i in login_res.keys():
                        payload += ((i, login_res[i]),)

                if type(login_res) == dict:
                    response = requests.request(api_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload)


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
                    response = requests.request(api_method.upper(), url, headers=header, data=payload)
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=payload)


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
                    response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
                else:
                    response = login_res.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))

            response.encoding = "utf-8"
            res = response.text

            DB_host.objects.update_or_create(host=api_host)

        print('【返回体】：',res )

        # 对返回值res进行提取：

        # # 路径法提取：
        if get_path != '': #说明有设置
            for i in get_path.split('\n'):
                key = i.split('=')[0].rstrip()
                path = i.split('=')[1].lstrip()

                py_path = ""
                for j in path.split('/'):
                    if j !='':
                        if j[0] != '[':
                            py_path += '["%s"]'%j
                        else:
                            py_path += j
                value = eval("%s%s" % (json.loads(res), py_path))
                exec('global %s\n%s = value '%(key,key))
        # # 正则法提取：
        if get_zz != '': #说明有设置
            for i in get_zz.split('\n'):
                key = i.split('=')[0].rstrip()
                zz = i.split('=')[1].lstrip()
                value = re.findall(zz,res)[0]
                exec('global %s\n%s = "%s" '%(key,key,value))

        # 对返回值res进行断言：

        ## 断言-路径法
        if assert_path != '' :#说明有设置
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
                self.assertEqual(want,value,'值不等')


        ## 断言-正则
        if assert_zz != '':
            for i in assert_zz.split('\n'):
                zz = i.split('=')[0].rstrip()
                want = i.split('=')[1].lstrip()
                value = re.findall(zz,res)[0]
                self.assertEqual(want,value,'值不等')


        ## 断言-全值
        if assert_qz != '':
            for i in assert_qz.split('\n'):
                if i not in res:
                    raise AssertionError('字符串不存在：%s'%i)



def make_defself(step):
    def tool(self):
        Test.demo(self,step)
    setattr(tool,"__doc__",u"%s"%step.name)
    return tool


def make_def(steps,Case_id):
    Test.Case_id = Case_id
    for fun in dir(Test):
        if 'test_' in fun:
            delattr(Test,fun)

    for i in range(len(steps)):
        setattr(Test,'test_'+str(steps[i].index).zfill(3),make_defself(steps[i]))


def run(Case_id,Case_name,steps):
    make_def(steps,Case_id)
    suit = unittest.makeSuite(Test)
    filename = 'MyApp/templates/Reports/%s.html'%Case_id
    fp = open(filename,'wb')
    runner = HTMLTestRunner(fp,title='接口测试平台测试报告: %s'%Case_name,description='用例描述')
    runner.run(suit)

