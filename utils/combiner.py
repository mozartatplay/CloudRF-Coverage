import sys
import os
import time
import json
import subprocess
import argparse
import requests
import glob
from json import load, JSONEncoder
from optparse import OptionParser
from re import compile


# General command line
def cmd_call (paramlist):
	out = subprocess.Popen(paramlist,
			stdout=subprocess.PIPE, 
			stderr=subprocess.STDOUT).wait()



def cmd_run (paramstr):
	os.system(paramstr)

# Function to extract shapefiles
def extract_shapefiles(shapefiles):
   
	if not os.path.exists("extract"):
		os.makedirs("extract")

	for shapefile in shapefiles:
			print ('Processing shapefile: ',shapefile)
			print ('Unzipping zipped file: ', shapefile)

			# Unzip files to extract directory
			plist = ['unzip', '-d', 'extract', '-o', shapefile]
			cmd_call(plist)
			
			
			# Mv all files from extract directory
			shapename = os.path.splitext(shapefile)[0]
			basefile = os.path.splitext(shapename)[0]
			shp_file = basefile + '.shp'
			shx_file = basefile + '.shx'
			prj_file = basefile + '.prj'
			dbf_file = basefile + '.dbf'
			print(basefile)
			print ('rename files: ', shapefile)
			plist = ['mv', '-f', 'extract/coverage.shp', shp_file]
			cmd_call(plist)
			plist = ['mv', '-f', 'extract/coverage.shx', shx_file]
			cmd_call(plist)
			plist = ['mv', '-f', 'extract/coverage.prj', prj_file]
			cmd_call(plist)
			plist = ['mv', '-f', 'extract/coverage.dbf', dbf_file]
			cmd_call(plist)

# Function to combine tiff
def combine_tiff(tiffPath, tiffCombineName):
	#print (tiffPath, tiffCombineName)
	# Unzip files to extract directory

	# Check for exisitance of files
	fcheck =  glob.glob(tiffPath)

	# Break up files
	print (fcheck)


	if len(fcheck) > 0: 
		tempcombine = os.path.splitext(tiffCombineName)[0] + '_temp.tiff'
		print ('Running combiner on: ', tiffPath)
		pstr = 'gdal_merge.py -co compress=LZW -o ' + tempcombine + ' ' + tiffPath
		#plist = ['gdal_merge.py', '-co', 'compress-LZW', '-o', './tempcombine.tiff', tiffPath]
		cmd_run(pstr)
		
		#gdal_merge.py -co compress-LZW -o test.tiff MALAWI2G_900_itm_rxs95_cll_default_ant_kathrein_742266_5dbi_cable_loss__2/*.tiff
		
		# Shrink tiff
		pstr = 'gdal_translate -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=2 ' + tempcombine + ' ' + tiffCombineName
		#plist = ['gdal_translate', '-of', 'GTiff', '-co', 'COMPRESS=DEFLATE', '-co', 'PREDICTOR=2', './tempcombine.tiff', tiffCombineName]
		cmd_run(pstr)
		#gdal_translate -of GTiff -co "BIGTIFF=YES" -co "COMPRESS=DEFLATE" -co "PREDICTOR=2" test.tiff test_small.tiff

		# remove old temp file
		#plist = ['rm', './tempcombine.tiff']
		#pstr = 'rm ' + tempcombine
		cmd_run(pstr)
	else:
		print ('No files matching: ', tiffPath)
		print ()


# Function to generate geo json
def create_geojson(tiffCombineName, geojsonName):
	# Create GeoJSON version of file
	#print (tiffCombineName, geojsonName)
	# Check for exisitance of files
	fcheck =  glob.glob(tiffCombineName)


	if len(fcheck) > 0: 
		print ('Running GeoJson generator on: ', tiffCombineName)
		#plist = ['gdal_polygonize.py', 'f', 'GeoJSON”', tiffCombineName, geojsonName]
		pstr = 'gdal_polygonize.py -f GeoJSON ' + tiffCombineName + ' ' + geojsonName
		cmd_run(pstr)
		# gdal_polygonize.py -f "GeoJSON” [inputfile].tiff [outputfile].geojson

	else:
		print ('No files matching: ', tiffCombineName)
		print ()

# Functions to build mesh

def mesh(uid,net):
	r = requests.get(server+"/API/mesh/?uid="+str(uid)+"&network="+net)
	print(r.text)
	if not ('mesh job' in r.text):
		j = json.loads(r.text)
		if 'filename' in  j:
			fname = j['filename']
			print(fname)
			# Write wsg84 png
			if 'png_wgs84' in j:
				png_url = j['png_wgs84']
				print ('Getting PNG: ', png_url)
				r = requests.get(png_url)
				file = open("networks"+os.sep+fname+'.png',"wb")
				file.write(r.content)
			return fname
		else:
			return ""
	else:
		return ""



def archiveDL(uid,key,fname,fileformat):
	dlargs={'uid': uid, 'key': key, 'file': fname, 'fmt': fileformat}
	r = requests.get(server+"/API/archive/data.php", params=dlargs)
	#file = open("networks"+os.sep+fname+"."+fileformat,"wb")
	file = open("networks"+os.sep+fname+".zip","wb")
	file.write(r.content)
	file.close()
	print("Wrote %d bytes to %s.%s" % (len(r.text),fname,fileformat))


def merge_geojson(geojsonPath, outfile):
	float_pat = compile(r'^-?\d+\.\d+(e-?\d+)?$')
	charfloat_pat = compile(r'^[\[,\,]-?\d+\.\d+(e-?\d+)?$')
	precision=6

	infiles = glob.glob(geojsonPath)
	outjson = dict(type='FeatureCollection', features=[])
	
	for infile in infiles:
		injson = load(open(infile))
		
		if injson.get('type', None) != 'FeatureCollection':
			raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)
		
		if type(injson.get('features', None)) != list:
			raise Exception('Sorry, "%s" does not look like GeoJSON' % infile)
		
		outjson['features'] += injson['features']

	encoder = JSONEncoder(separators=(',', ':'))
	encoded = encoder.iterencode(outjson)
	
	format = '%.' + str(precision) + 'f'
	output = open(outfile, 'w')
	
	for token in encoded:
		if charfloat_pat.match(token):
			# in python 2.7, we see a character followed by a float literal
			output.write(token[0] + format % float(token[1:]))

		elif float_pat.match(token):
			# in python 2.6, we see a simple float literal
			output.write(format % float(token))

		else:
			output.write(token)


parser = argparse.ArgumentParser()
#group = parser.add_mutually_exclusive_group()
parser.add_argument("path",  help="Path to tiff files")
parser.add_argument("-g", "--geojson", action="store_true", default=False, help="create geojson" )
parser.add_argument("-s", "--split", action="store_true", default=False, help="split files for fast processing" )
args = parser.parse_args()

path_calc =   args.path
net_path_arr = path_calc.split('/')
print(net_path_arr)
net_path = net_path_arr[len(net_path_arr)-2]
print(net_path)

search_path = path_calc  + '*.tiff'
tiffCombineName = path_calc  + net_path + '.tiff'
geojsonName = path_calc + net_path + '.geojson'

if not args.split:
	print ('Runing Tiff combiner and shrinker .... ')
	combine_tiff(search_path, tiffCombineName)

	if args.geojson:
		print ('Converting combined Tiff to GeoJson ... ')
		create_geojson(tiffCombineName,geojsonName)
else:
	print ('Running split Tiff combiner and shrinker ....')
	for i in range(1,10):
		search_path = path_calc  + str(i) + '*.tiff'
		tiffCombineName = path_calc  + net_path + "_" + str(i) + '.tiff'
		geojsonName = path_calc + net_path + "_" + str(i) + '.geojson'
		print ('Running combiner for files:  ', search_path)
		combine_tiff(search_path, tiffCombineName)


		if args.geojson:
			print ('running Tiff to GeoJson for Tiff: ', tiffCombineName)
			create_geojson(tiffCombineName,geojsonName)

	print ('Running Complete Geojson combiner ... ')
	geojsonPath = path_calc  + '*.geojson'
	geojsonOut = path_calc + net_path + '_final' + '.geojson'
	merge_geojson(geojsonPath,geojsonOut)
	print ('PROCESS COMPLETE')