#!/usr/bin/python
import requests

# Programmatically delete a calculation by name OR network

server="https://cloudrf.com"
strictSSL=False

uid=str(28915)
key="3ac099165b846b48ecb8e59d1835eee2eeb3f33c"
network="NAMIBIA3G__2"

start_id = 1220180543
gap = 8

for 
# Delete by name..
req = requests.get(server+"/API/archive/data.php?uid="+uid+"&key="+key+"&delete=12345_NETWORK_SITE",verify=strictSSL)
result = req.text
print(result)

# Delete by network..
req = requests.get(server+"/API/archive/data.php?uid="+uid+"&key="+key+"&nid="+network+"&del=1",verify=strictSSL)
result = req.text
print(result)
