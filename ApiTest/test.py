import requests

url = "http://www.baidu.com"

payload= (
    ("a","1"),
    ("a","2"),
    ("a","3"),
    ("b","5"),
)

print(payload)


files=[

]
headers = {
  'Cookie': 'BAIDUID=6C6C6030F1690FD7425DECAAA7BB547E:FG=1; BDSVRTM=0'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.request.body)
