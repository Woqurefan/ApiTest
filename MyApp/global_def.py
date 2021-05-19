# coding:utf-8

# 本文件存储公共方法
# 请按规则传入和接收
from MyApp.models import *
import re
import ast #安全版eval求值

# 替换全局变量
def global_datas_replace(project_id:str,s:str) -> str :
    #根据项目变量去获得生效的变量组。
    try:
        global_data_ids = DB_project.objects.filter(id=project_id)[0].global_datas.split(',') #获取所有生效的变量组id
    except:
        return s

    if global_data_ids == ['']:
        return s

    global_datas = {}
    for i in global_data_ids:
        global_data = ast.literal_eval(list(DB_global_data.objects.filter(id=i).values())[0]['data'])
        global_datas.update(global_data)
    # 最终的gloabl_datas就是总变量池字典了
    #用正则找出所有需要替换的变量名称​。
    # 处理url/header/data
    list_data = re.findall(r'~(.*?)~',s)
    for i in list_data:
        s = s.replace('~'+i+'~',str(global_datas[i]))
    #返回结果。
    return s


