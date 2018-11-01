#!/usr/bin/env python

import netCDF4
import sys
import os
import numpy as np
import struct
import argparse
from datetime import datetime, timedelta
import pytz
import string
import pycurl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm

# https://matplotlib.org/basemap/users/examples.html

def main():
    parser = argparse.ArgumentParser(description='Read data from met.no and write IEEE.')
    parser.add_argument('--version', action='version', help='Show version')
    parser.add_argument('-v', '--verbose', action='count', help='Set verbose')

    global verbose
    args = parser.parse_args()
    verbose = args.verbose

    ## Today
    dt = datetime.utcnow()
    url = ('https://thredds.met.no/thredds/dodsC/remotesensing/reflectivity-nordic/{0}/{1}/yrwms-nordic.mos.pcappi-0-dbz.noclass-clfilter-novpr-clcorr-block.laea-yrwms-1000.{0}{1}{2}.nc'
        .format(dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d"))
    )
    print "[INFO] URL: '{}'".format(url)
    ## Fetch the data
    readData(url)


def readData(url):
    # create a dataset object
    try:
        dataset = netCDF4.Dataset(url)
    except:
        print "[ERROR]: Could not connect to URL: %s" % url
        sys.exit(255)

    timezone = pytz.timezone("utc")

    timesteps = dataset.variables['time']
    DataTime_naive = datetime.utcfromtimestamp(timesteps[-1])
    DataTime = timezone.localize(DataTime_naive)
    print "[INFO] Last Time: '{}'".format(DataTime)
    print

    print "Projection details:"
    projection = dataset.variables['projection_lambert']
    print "GridMappingName: '%s'" % projection.grid_mapping_name
    print "LonOfCentMeridian: '%s'" % projection.longitude_of_central_meridian
    print "LatOrign: '%s'" % projection.latitude_of_projection_origin
    print "Proj4: '%s'" % projection.proj4
    print

    parameters = ["equivalent_reflectivity_factor"]
    for param in parameters:
        variable = dataset.variables[param]
        if verbose >= 3:
            print param,"->shape: ",variable.shape
            print param,"->long_name: ",variable.long_name
            print param,"->units: ",variable.units
            print param,"->standard_name: ",variable.standard_name

            print
            print variable
            print

        time_slices = variable.shape[0]
        print ("Time slices: {}".format(time_slices))
        DataTime_naive = datetime.utcfromtimestamp(timesteps[-1])
        DataTime = timezone.localize(DataTime_naive)

        filetime = DataTime.strftime("%Y%m%d%H%M")
        # Get the data variable from URL
        print "[INFO]: Fetching data..."
        data_array = dataset.variables[param][-1]

        print "[INFO]: Timestep: '{0}' Min(Value): '{1}' Max(Value): '{2}'".format(filetime, np.min(data_array), np.max(data_array))
        #sys.exit(0)

        draw_map(data_array, filetime)

    dataset.close()

def draw_map(data, time):
    map = Basemap(projection='cyl',llcrnrlon=0,llcrnrlat=50, urcrnrlon=30, urcrnrlat=75,resolution='l')#,
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
#    map.fillcontinents(color='coral',lake_color='blue')
    # draw the edge of the map projection region (the projection limb)
#    map.drawmapboundary(fill_color='aqua')
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0,360,10))
    map.drawparallels(np.arange(-90,90,10))

    ny = data.shape[0]; nx = data.shape[1]
    lons, lats = map.makegrid(nx, ny) # get lat/lons of ny by nx evenly space grid.
    x, y = map(lons, lats) # compute map proj coordinates.
    # draw filled contours.
    clevs = [0,1,2.5,5,7.5,10,15,20,30,40,50,70,100,150,200,250,300,400,500,600,750]
    cs = map.contourf(x,y,data,clevs,cmap=cm.s3pcpn)
    # add colorbar.
    cbar = map.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('mm')

    plt.title('Radar at {}'.format(time))
    plt.show()







if __name__ == "__main__":
    main()
    sys.exit(0)
