# radiocoverage calculation tool
Calculate coverage with Cloudrf Cloud API

# INSTALLATION

## Install GDAL tools
### For MACOSX
If you haven't installed Homebrew
```
$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)
```


From home directory
```
brew install gdal
cd ~
mkdir python-virtual-env
cd python-virtual-env
python3 -m venv env
source ~/python-virtual-env/env/bin/activate
pip3 install numpy
pip3 install gdal==$(gdal-config --version)
```
### For Ubuntu
From home directory
```
mkdir python-virtual-env
cd python-virtual-env
python3 -m venv env
source ~/python-virtual-env/env/bin/activate
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip3 install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
```

## Install dependencies for cloudrf_coverage 
pip3 install pyshp commentjson requests

# USAGE
```
usage: cloudrf_coverage.py [-h] [-a ANTENNA] [-c] [-t] [-d DELIMETER]
                           site_data calc_constants

positional arguments:
  site_data             List of cell sites
  calc_constants        Calculation constants for run

optional arguments:
  -h, --help            show this help message and exit
  -a ANTENNA, --antenna ANTENNA
                        Provide an antenna file for run
  -c, --cont            Continue a previous run
  -t, --test            Do a test run without live calculations
  -d DELIMETER, --delimeter DELIMETER
                        Change the delimeter for CSV files - default is ','
                        Use single quotes around delimeter
```

# DESCRIPTION

Cloudrf_coverage.py calls the CloudRF API (https://api.cloudrf.com/) using the input files. You will need to register an account at CloudRF before using this tool. Each cellID row in Celldata-file is used to generate a coverage plot for that specific CellID and combination of parameters in Config-file and Antenna-file. The output coverage for each cell is placed in a folder ./calculations/[network_name] where the network_name is set in the calculations constants file under the ['network_constants']['net'] field  

If a 'tiff' file format is specified in the calculations constants file. A combined coverage will be calculated using GDAL tools and the final result will be placed in the calculations folder

# Compulsary OPTIONS

## site_data:
 A csv file containing all the cell data provided by the operator with field values defined in Config-file
## calc_constants: 
A json formatted file containing CloudRF general and network parameters as well as antenna default values and cell data field mappings.  

Make sure you change these fields to those provide by CloudRF
```
// uid (Unique user identifier. Your CloudRF account id number.): 
"uid": <Your CloudRF ID>
// key (Unique API key)  :  (Unique API key.)
"key": <Your CloudRF key>,
```

# Optional OPTIONS

## (--antenna) ANTENNA: 
A csv file containing antenna and frequency to CloudRF ID mappings
## (--cont)
Setting this option will cause cloudrf to continue a previous interrupted run and not create a new folder
## (--test)
Setting this option will run through the entire cell list in the site_data file and not call the cloudRF API. This is useful for checking if all your parameters have been set correctly
## (--delimeter)
This allows you to change the delimeter used in CSV files. The detault is ',' but ';' is often used. Remember to place the new delimeter in single quotes

# how to access virtal python environment
source ~/python-virtual-env/env/bin/activate 
## then navigate to folder with all the files and run the command. To exit: 
deactivate

# EXAMPLES

### Example 1 A new run where detault antenna is used 
```
python3 cloudrf_coverage.py test_coords.csv calculation_constants_test.json -d ';'
```
### Example 2 A continuation run with a default antenna 
```
python3 cloudrf_coverage.py test_coords.csv calculation_constants_test.json -c -d ';'
```
### Example 3 A test run to see if all settings are correct with default antenna 
```
python3 cloudrf_coverage.py test_coords.csv calculation_constants_test.json -t -d ';'
```
### Example 4 A new run using a supplied antenna file 
```
python3 cloudrf_coverage.py test_coords.csv calculation_constants_test.json -a antenna_test.csv -d ';'
```


# NOTES for setting values in config file

rxs threshold should match blue if using col=7
rxs threshold is used as the edge for single color plots (col=2)

