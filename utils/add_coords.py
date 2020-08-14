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



server="https://cloudrf.com"

if (len(sys.argv) <3 ):
	print ("usage: python3 add_coords <cell_data.csv> <site_data.csv>")
	print ("")
	quit()

cellfile = sys.argv[1]
cellfile_FP = open(cellfile, mode="r", encoding="latin-1")
cellfile_data = csv.DictReader(cellfile_FP, delimiter=",")
sitefile = sys.argv[2]
sitefile_FP = open(sitefile)
sitefile_data = csv.DictReader(sitefile_FP, delimiter=",")

def search(Litem,Ldict):
	
	for i in Ldict:
		if i["PK_Site_ID"].strip() == Litem:
			return i
	return None

ofn = cellfile.split('.')[0] + "_coords" + '.csv'

of = open(ofn,"w")
of.write("cellID,latitude,longitude,band,antenna,height,azimuth,etilt,mtilt" + "\n")

for row in cellfile_data:
	# Find coordinates from site file
	sitefile_FP.seek(0)
	match =  search(row["Site_ID"],sitefile_data)
	print ("Checking ID: ", row["Site_ID"].strip())
	if (not match):
		print ("No coordinate found for site: ", row["Site_ID"].strip())
		latitude = "none"
		longitude = "none"
	else:
		latitude = match["Latitude"].strip()
		longitude = match["Longitude"].strip()
	# Create new row
	newrow = row['Cell_ID'].strip() + "," + latitude + "," + longitude + "," + "900E" + "," + row['Antenna_model'].strip() + "," + row['Antenna_Height'].strip() + "," + row['Azimuth'].strip() + ",0," + row['Tilt'].strip() + "\n"
	of.write(newrow)
	

of.close()

