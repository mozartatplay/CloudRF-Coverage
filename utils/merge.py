import shapefile as pyshp
import os
import glob
import time

import subprocess


#cmd = 'unzip -o 21221.shp.zip'
#os.system(cmd)



def merge_shapefiles(shapefiles, out_shapefile):
    '''Merge shapefiles into one'''

    cmd = 'unzip'

    with pyshp.Writer(out_shapefile) as shp_writer:
        for shapefile in shapefiles:
                print ('Processing shapefile: ',shapefile)
                out = subprocess.Popen([cmd, '-o', shapefile], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
                out.wait()
                with pyshp.Reader('./coverage.shp') as shp_reader:
                    if not shp_writer.fields:
                        shp_writer.fields = shp_reader.fields[1:]
                    for shp_record in shp_reader.iterShapeRecords():
                        shp_writer.record(*shp_record.record)
                        shp_writer.shape(shp_record.shape)

shpf_list = glob.glob("*.zip")
print(shpf_list)

shpf_out = './merge.shp'
merge_shapefiles(shpf_list,shpf_out)
