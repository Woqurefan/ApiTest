s = '21312313'
import json


a = {"a":1}

b = {"b":2}


# a.update(b)
print({"a":1,**b})