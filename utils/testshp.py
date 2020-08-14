import shapefile as pyshp
import os
import glob
import time
import sys
import subprocess


#cmd = 'unzip -o 21221.shp.zip'
#os.system(cmd)

fileC = open('file_corrupt.log','w')

cmd = 'rm'

def check_shapefiles(shapefiles,delOption):
    '''Check shape files'''

    mkstr = "mkdir ./corrupt"
    subprocess.call(mkstr, shell=True)


    for shapefile in shapefiles:
        subfile = shapefile.split('.')[0]
        searchsubfile = subfile + '.*'
        #print (searchsubfile)
        try:    
            with pyshp.Reader(shapefile) as shp_reader:
                fieldTot = 0
                #print ('Testing Shapefile: ',shapefile)
                for shpitem in shp_reader.iterShapeRecords():
                    fieldTot += 1

                
                
                #print('Total fields:  ', fieldTot)
                if fieldTot == 0:
                    print ('Found zero length file: ',shapefile)
                    fstr = 'Zero length file: ' + shapefile + '\n'
                    if delOption == 'del':
                        print ('moving files:  ' + searchsubfile)
                        delstr = 'mv ' + searchsubfile + ' ./corrupt'
                        print (delstr)
                        subprocess.call(delstr, shell=True),
                        
                    fileC.write(fstr)
        except:
            print ('Corrupt file cant read: ',shapefile)
            if delOption == 'del':
                print ('moving files:  ' + searchsubfile)
                delstr = 'mv ' + searchsubfile + ' ./corrupt'
                print (delstr)
                subprocess.call(delstr, shell=True),
                
            fstr = 'Corrupt file: ' + shapefile + '\n'

            fileC.write(fstr)

shpf_list = glob.glob("*.shp")
#print(shpf_list)
print ('Testing shape files .... ')
print


if (len(sys.argv) !=2 ):
	print ("usage: python3 testshp.py <del|nodel>")
	print ("")
	quit()

delOption = sys.argv[1]
check_shapefiles(shpf_list,delOption)


