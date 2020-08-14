
import requests
import csv
import sys
import os
import time
import json
import commentjson
import re
import arfcn_lib
import re
import constants
import shapefile as pyshp
import glob
import subprocess



if (len(sys.argv) != 2 ):
    print ("usage: python3 fetch_images <network name>")
    print ("")
    quit()



## Load Constants from file
netfile = sys.argv[1]


#url=https://cloudrf.com/API/archive/data.php?uid=28915&key=3ac099165b846b48ecb8e59d1835eee2eeb3f33c&band=all&n=80&e=180&s=-80&w=-180&network=MALAWI2G_900_itm_rxs95_cll_default_ant_kathrein_742266_5dbi_cable_loss__1

server="https://cloudrf.com/API/archive/data.php"
p={
    "uid":28915, 
    "key":"3ac099165b846b48ecb8e59d1835eee2eeb3f33c",
    "band":"all",
    "n":80,
    "e":180,
    "s":-80,
    "w":-180,
    "network":netfile
}
#p=(('uid,','28915'),('key','3ac099165b846b48ecb8e59d1835eee2eeb3f33c'),('band','all'),('n','80'),('e','180'),('s','-80'),('w','-180'),('network','MALAWI2G_900_itm_rxs95_cll_default_ant_kathrein_742266_5dbi_cable_loss__1'))
### Run calculation for area
r = requests.get(server,params=p)
#print (r.content)
#j = json.loads(r.text)
#print(j)
### Run calculation for area

path_calc = "./fetch_images/" + p['network']

if not os.path.exists(path_calc):
    os.makedirs(path_calc)

rj = json.loads(r.text)
calcs = rj['calcs']

if len(calcs) == 0:
    print ('Network not found')
    print ("")
else:
    print ('Total images to retrieve: ', len(calcs))

