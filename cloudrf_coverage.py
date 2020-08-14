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
import argparse

from json import load, JSONEncoder
from optparse import OptionParser
from re import compile

server="https://cloudrf.com"

# General command line
def cmd_call (paramlist):
    out = subprocess.Popen(paramlist,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT).wait()

'''
def cmd_run (paramlist):
	out = subprocess.run(paramlist,
				stdout=subprocess.PIPE, 
				stderr=subprocess.STDOUT)
	print (out)
'''

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
		#plist = ['rm', tempcombine]
		pstr = 'rm ' + tempcombine
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


def FindAntenna_arfcn (antennas, type, dlfreq):
	for antenna in antennas:
		if antenna['Antenna Type']==type and int(antenna['Dl Freq'])==int(dlfreq):
			return [antenna['CloudRFID'],antenna['Gain']]
	else:
		return [0,0]

def FindAntenna_band (antennas, type, band):
	for antenna in antennas:
		if antenna['Antenna Type']==type and int(antenna['Band'])==int(dlfreq):
			return [antenna['CloudRFID'],antenna['Gain']]
	else:
		return [0,0]



parser = argparse.ArgumentParser()
#group = parser.add_mutually_exclusive_group()
parser.add_argument("site_data",  help="List of cell sites")
parser.add_argument("calc_constants",  help="Calculation constants for run")
parser.add_argument("-a", "--antenna", default='none', help="Provide an antenna file for run" )
parser.add_argument("-c", "--cont", action="store_true", default=False, help="Continue a previous run")
parser.add_argument("-t", "--test", action="store_true", default=False, help="Do a test run without live calculations")
parser.add_argument("-d", "--delimeter", default=',', help="Change the delimeter for CSV files - default is ',' Use single quotes around delimeter")
args = parser.parse_args()


continue_run = args.cont
test_run = args.test
if (args.antenna=='none'):
	default_antenna = True
else:
	default_antenna = False
	antennafile = args.antenna

configfile = args.calc_constants
sitefile = args.site_data
delimeter = args.delimeter

if not os.path.exists("calculations"):
		os.makedirs("calculations")

if not os.path.exists("networks"):
		os.makedirs("networks")

## Load Constants from file
with open(configfile) as json_file:
	calculation_constants = commentjson.load(json_file)

# Load antenna data from file
if not(default_antenna):
	antennadata = list(csv.DictReader(open(antennafile), delimiter=delimeter))

fileformat =  calculation_constants['general_constants']['file']
cloudrf_network = calculation_constants['network_constants']['net']

## Check the current network iterator and iterate

net_path = './calculations'
files = []
# r=root, d=directories, f = files
netIndex = 1

for r, d, f in os.walk(net_path):
	for directory in d:
		if cloudrf_network in directory:
			r1 = re.findall(r"__\d+",directory)
			if (r1):
				r2 = re.findall(r"\d+",r1[0])
				if (int(r2[0]) >= netIndex):
					if not continue_run:
						netIndex = int(r2[0])+1
					else:
						netIndex = int(r2[0])



print ()
print ('Network Name: ', cloudrf_network)           
print('Current Network Index Nunber: ', netIndex)
print ('Using file format: ',fileformat)


# Add the network index to the network name
calculation_constants['network_constants']['net'] = calculation_constants['network_constants']['net'] + "__" + str(netIndex)


# Create network folder in calculations

path_calc =  "calculations" + os.sep + calculation_constants['network_constants']['net']

if not test_run:
	if not os.path.exists(path_calc):
		os.makedirs(path_calc)

	# Create a file to store all calculation URLS
	fn=path_calc+os.sep+"calculation_urls"
	furls = open(fn,"a")

# If continue - Check if any calculations already completed
ignore_list = []

if continue_run:
	if fileformat == 'shp':
		search_path = path_calc + os.sep + '*.zip'
	if fileformat == 'tiff':
		search_path = path_calc + os.sep + '*.tiff'

	file_list = glob.glob(search_path)

	print ('List of files to ignore:')
	for f in file_list:
		print (os.path.basename(f))
		fn = os.path.basename(f).split('.')[0]
		ignore_list.append(fn)




# Read in bounding box
min_lon =  float(calculation_constants['bounding_box']['top_left']["lon"])
max_lon = float(calculation_constants['bounding_box']['bottom_right']["lon"])
min_lat = float(calculation_constants['bounding_box']['bottom_right']["lat"])
max_lat = float(calculation_constants['bounding_box']['top_left']["lat"])

print ("Bounding box (Lat,long): Top LEFT: (",min_lat,",",min_lon,") Bottom RIGHT: (",max_lat,",",max_lon,")")

# Read in the csv of all Cell Info

csvfile = csv.DictReader(open(sitefile), delimiter=delimeter)
# Read in the csv of all Cell Info

print ()
n=0
network_parameters = {}
for row in csvfile:
	#print (row)
	# Check if in bounding box
	### Latitude
	fieldN = calculation_constants['celldata_field_mappings']['lat']
	latitude = row[fieldN]
	

	### Longitude
	fieldN = calculation_constants['celldata_field_mappings']['lon']
	longitude = row[fieldN]
	
	
	fieldN = calculation_constants['celldata_field_mappings']['nam']
	CellID = row[fieldN]

	
		
	### Network name
	
	network_parameters['nam'] = CellID
	print('Processing CellID: ', CellID, " at position: ", latitude, longitude)

	#print ('Checking file: ',CellID, ' lat: ', latitude, ' lon: ', longitude)
	if CellID in ignore_list:
		print ('Skipping CellID: ', CellID)

	if not(float(latitude) > min_lat and float(latitude) < max_lat and float(longitude) > min_lon and float(longitude) < max_lon):
		print ('Cell ID outside bounding box')

	# Check if in bounding box and not in ignore list
	if (float(latitude) > min_lat and float(latitude) < max_lat and float(longitude) > min_lon and float(longitude) < max_lon) and (not CellID in ignore_list): 
		network_parameters['lat'] = latitude
		network_parameters['lon'] = longitude

		# Pause script. Important otherwise server will ban you.
		if not test_run:
			time.sleep(1)
			start_time = time.time() # Stopwatch start
		


		### Extract bandwidth - if none - set to 1
		fieldN = calculation_constants['celldata_field_mappings']['bw']
		if fieldN != "none":
			bw = row[fieldN]
			# Strip non alhpa
			bwi = ''.join(re.findall(r'\d+', bw))
			network_parameters['bwi'] = bwi
		
		
		### Calculate downlink frequency and associated antenna data from AFRCN number or from Band
		#Extract antenna type
		fieldN = calculation_constants['celldata_field_mappings']['antennaT']
		if fieldN=='none' or default_antenna:
			antennaType = "none"
		else:
			antennaType = row[fieldN]

		fieldN = calculation_constants['celldata_field_mappings']['band']
		if fieldN == "none":
			# Calculate frequency from downlink ARFCN
			tech = calculation_constants['network_constants']['tech']
			fieldN = calculation_constants['celldata_field_mappings']['arfcn_d']
			if fieldN == "none":
				print ('Need at least a Band or an ARFCN number')
				exit()
			else:
				arfcn = row[fieldN]
				# Run conversion
				Dfreq = arfcn_lib.ArfcnToFreq(tech, arfcn)
				if (Dfreq == 0):
					print ('ARFCN number not found')
					exit()
				else:
					network_parameters['frq'] = str(round(Dfreq))
					# Extract antenna info from antenna type and frequency
					if (default_antenna):
						antennaSet = [0,0]
					else:
						antennaSet =  FindAntenna_arfcn(antennadata,antennaType,arfcn)

		else:
			# Calculate middle of downlink frequency range and set as frequency
			band = row[fieldN]
			# is band in dictionary
			if band in constants.frequency_bands:
				mid_down = (constants.frequency_bands[band]['downlink']['end'] + constants.frequency_bands[band]['downlink']['start'])/2 
				network_parameters['frq'] = str(round(mid_down))
				if (default_antenna):
					antennaSet = [0,0]
				else:		
					antennaSet =  FindAntenna_band(antennadata,antennaType,band)
			else:
				print ('Band not found can not continue')
				exit()


		### Extract antenna information
		antennaID = antennaSet[0]
		antennaGain = antennaSet[1]

		# If no antenna found then use default
		if int(antennaID) == 0:
			antennaID = calculation_constants['antenna_constants']['default_antenna']
			antennaGain = calculation_constants['antenna_constants']['default_gain']
	


		### Antenna type code - linked to CloudRF ID
		network_parameters['ant'] = str(antennaID)

		### Transmitter gain from antenna specs
		network_parameters['txg'] = str(antennaGain)

		### Transmitter height
		fieldN = calculation_constants['celldata_field_mappings']['txh']
		network_parameters['txh'] = row[fieldN]

		### Azimuth of antenna 
		fieldN = calculation_constants['celldata_field_mappings']['azi']
		network_parameters['azi'] = row[fieldN]

		### Tilt of antenna = mechanical  electrical tilt
		fieldN = calculation_constants['celldata_field_mappings']['etilt']
		etilt = row[fieldN]

		fieldN = calculation_constants['celldata_field_mappings']['mtilt']
		mtilt =  row[fieldN]
		tilt = float(etilt) + float(mtilt)
		network_parameters['tlt'] = str(round(tilt))

		#print(network_parameters)

		### Add all the RFCLOUD parameters together
		rfcloud_params = dict(calculation_constants['general_constants'], **calculation_constants['network_constants'], **network_parameters)
		print (rfcloud_params)
		rfcloud_params_tuples = list(rfcloud_params.items()) 
		#print (rfcloud_params_tuples)



		### Run calculation for area

		if not test_run:
			try: 
				r = requests.post(server+"/API/area", data=rfcloud_params)
				print(r.text)
				j = json.loads(r.text)


				# Write out file in correct format
				if 'kmz' in j:
					#print j['kmz']
					furls.write(j['kmz']+"\n")
					r = requests.get(j['kmz'])
					fn=path_calc+os.sep+str(rfcloud_params['nam'])+".kmz"
					filename = open(fn,"wb")
					filename.write(r.content)
					filename.close()
					print("Saved to %s" % fn)
				if 'shp' in j:
					#print j['kmz']
					furls.write(j['shp']+"\n")
					r = requests.get(j['shp'])
					fn=path_calc+os.sep+str(rfcloud_params['nam'])+".shp.zip"
					filename = open(fn,"wb")
					filename.write(r.content)
					filename.close()
					print("Saved to %s" % fn)

				if 'tiff' in j:
					#print j['kmz']
					furls.write(j['tiff']+"\n")
					r = requests.get(j['tiff'])
					fn=path_calc+os.sep+str(rfcloud_params['nam'])+".tiff"
					filename = open(fn,"wb")
					filename.write(r.content)
					filename.close()
					print("Saved to %s" % fn)

				elapsed = round(time.time() - start_time,1) # Stopwatch
				print("Elapsed: "+str(elapsed)+"s")
			except:
				print ("Can't connect to cloudRF database ...")
				quit()
		
		
		n=n+1
		print()

print()
print('Total calculations: ', n)
print()
	
# Mesh the resulting network

'''print()
print('Calculating Mesh for network')
print('----------------------------')
print()
uid = calculation_constants['general_constants']['uid']
key = calculation_constants['general_constants']['key']
net = calculation_constants['network_constants']['net']


fname = mesh(uid,net)
archiveDL(uid,key,fname,fileformat) '''






if not test_run:
	furls.close()
	path_calc =  net_path + os.sep + calculation_constants['network_constants']['net']
	netname = calculation_constants['network_constants']['net']
	# If File type shape - unzip the shapefiles and rename
	if fileformat == 'shp':
		search_path = path_calc + os.sep + '*.zip'
		shpf_list = glob.glob(search_path)
		print(shpf_list)
		extract_shapefiles(shpf_list)


	# If tiff files - generate a combined zipped tiff plot and convert to geotiff
	if fileformat == 'tiff':
		'''search_path = path_calc + os.sep + '*.tiff'
		tiffCombineName = net_path + os.sep  + calculation_constants['network_constants']['net'] + '.tiff'
		geojsonName = net_path + os.sep + calculation_constants['network_constants']['net'] + '.geojson'

		print ('Runing Tiff combiner and shrinker .... ')
		combine_tiff(search_path, tiffCombineName)
		print ('Converting combined Tiff to GeoJson ... ')
		create_geojson(tiffCombineName,geojsonName)
		'''

		print ('Running split Tiff combiner and shrinker ....')
		for i in range(1,10):
			search_path = path_calc  + os.sep + str(i) + '*.tiff'
			tiffCombineName = path_calc  + os.sep + netname + '_' + str(i) + '.tiff'
			geojsonName = path_calc + os.sep + netname + "_" + str(i) + '.geojson'
			print ('Running combiner for files:  ', search_path)
			combine_tiff(search_path, tiffCombineName)

			
			print ('running Tiff to GeoJson for Tiff: ', tiffCombineName)
			create_geojson(tiffCombineName,geojsonName)
				
		
		print ('Running Complete Geojson combiner ... ')
		geojsonPath = path_calc  + os.sep + '*.geojson'
		geojsonOut = path_calc + os.sep + netname + '_final' + '.geojson'
		merge_geojson(geojsonPath,geojsonOut)
		print ('PROCESS COMPLETE')
	
