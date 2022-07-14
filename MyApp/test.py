
import json
s = '{"aaa":false}'

print(json.loads(s))

for i in json.loads(s).keys():
    print(s[i])