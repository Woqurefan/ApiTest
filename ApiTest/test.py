




a = "abc" # a是临时变量

d = '{"key": "##a##" }'  #d 是刚从数据库取出来的header 的json

new_d = d.replace("##a##",repr(str(a)))

print(new_d)