import json,re,requests

import unittest

h1 = "{'a':'a'}"
print(h1,type(h1))

h1 = json.dumps(eval(h1))
print(h1,type(h1))

h1 = json.loads(h1)
print(h1,type(h1))
