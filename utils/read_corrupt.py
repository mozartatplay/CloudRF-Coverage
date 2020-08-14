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

cfile = open('./file_corrupt_4g.log', 'r')
corrupt_cells = []
for line in cfile:
    lsplit = line.strip().split(' ')
    print (lsplit, len(lsplit))
    corrupt_cells.append(lsplit[len(lsplit)-1].split('.')[0]) 

print (corrupt_cells)
