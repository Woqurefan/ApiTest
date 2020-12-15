import json,re,requests

import unittest

from allpairspy import AllPairs
old = [['a','b'],['c','d'],['e','f']]

ready = []
for pairs in AllPairs(old[:2]):
    ready.append(''.join(pairs))
for i in range(2, len(old)):
  new_r= []
  for pairs in AllPairs([ready, old[i]]):
    new_r.append(''.join(pairs))
    ready=new_r

print(ready)
print(len(ready))