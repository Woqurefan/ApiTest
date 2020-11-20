# -*- coding:utf-8 -*-

import unittest,time,re,json,requests
from MyApp.A_WQRFhtmlRunner import HTMLTestRunner

class Test(unittest.TestCase):
    '测试类'

    def demo(self,step):
        time.sleep(3)
        print(step.api_url)
        # 提取所有请求数据
        api_method = step.api_method
        api_url = step.api_url
        api_host = step.api_host
        api_header = step.api_header
        api_body_method = step.api_body_method
        api_body = step.api_body
        get_path = step.get_path
        get_zz = step.get_zz
        assert_zz = step.assert_zz
        assert_qz = step.assert_qz
        assert_path = step.assert_path

        ## 检查是否需要进行替换占位符的
        rlist_url = re.findall(r"##(.+?)##",api_url)
        for i in rlist_url:
            api_url = api_url.replace("##"+i+"##",eval(i))

        rlist_header = re.findall(r"##(.+?)##",api_header)
        for i in rlist_header:
            api_header = api_header.replace("##"+i+"##",eval(i))

        rlist_body = re.findall(r"##(.+?)##",api_body)
        for i in rlist_body:
            api_body = api_body.replace("##"+i+"##",eval(i))

        ## 实际发送请求
        header = json.loads(api_header)  # 处理header
        # 拼接完整url
        if api_host[-1] == '/' and api_url[0] == '/':  # 都有/
            url = api_host[:-1] + api_url
        elif api_host[-1] != '/' and api_url[0] != '/':  # 都没有/
            url = api_host + '/' + api_url
        else:  # 肯定有一个有/
            url = api_host + api_url

        if api_body_method == 'none' or api_body_method=='null':
            response = requests.request(api_method.upper(), url, headers=header, data={})

        elif api_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload, files=files)

        elif api_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(api_body):
                payload[i[0]] = i[1]
            response = requests.request(api_method.upper(), url, headers=header, data=payload)

        else:  # 这时肯定是raw的五个子选项：
            if api_body_method == 'Text':
                header['Content-Type'] = 'text/plain'

            if api_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'

            if api_body_method == 'Json':
                header['Content-Type'] = 'text/plain'

            if api_body_method == 'Html':
                header['Content-Type'] = 'text/plain'

            if api_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(api_method.upper(), url, headers=header, data=api_body.encode('utf-8'))
        response.encoding = "utf-8"
        res = response.text

        # 对返回值res进行提取：


        # 对返回值res进行断言：











def make_defself(step):
    def tool(self):
        Test.demo(self,step)
    setattr(tool,"__doc__",u"%s"%step.name)
    return tool


def make_def(steps):
    for i in range(len(steps)):
        setattr(Test,'test_'+str(steps[i].index).zfill(3),make_defself(steps[i]))


def run(Case_id,Case_name,steps):

    make_def(steps)

    suit = unittest.makeSuite(Test)
    filename = 'MyApp/templates/Reports/%s.html'%Case_id
    fp = open(filename,'wb')
    runner = HTMLTestRunner(fp,title='接口测试平台测试报告: %s'%Case_name,description='用例描述')
    runner.run(suit)

