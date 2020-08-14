import shapefile as pyshp
import os
import glob
import time

import subprocess


#cmd = 'unzip -o 21221.shp.zip'
#os.system(cmd)

def cmd_call (paramlist):
    out = subprocess.Popen(paramlist,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT).wait()

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


       

shpf_list = glob.glob("*.zip")
print(shpf_list)

extract_shapefiles(shpf_list)
