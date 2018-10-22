#!/usr/bin/python

import sys
import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def main():
    parser = argparse.ArgumentParser(description='Testing testing.')
    parser.add_argument('--test', type=str)

    args = parser.parse_args()


    print "Peter {}".format(args.test)
    print "QWE: {}".format(np.__version__)

    # set up orthographic map projection with
    # perspective of satellite looking down at 50N, 100W.
    # use low resolution coastlines.
    map = Basemap(projection='ortho',lat_0=60,lon_0=15,resolution='l',
    llcrnrx=-90,llcrnry=0,urcrnrx=90.,urcrnry=90)
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='coral',lake_color='blue')
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='aqua')
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0,360,30))
    map.drawparallels(np.arange(-90,90,30))
    # make up some data on a regular lat/lon grid.
    nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
    lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
    lons = (delta*np.indices((nlats,nlons))[1,:,:])
    wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
    mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
    # compute native map projection coordinates of lat/lon grid.
    x, y = map(lons*180./np.pi, lats*180./np.pi)
    # contour data over the map.
    #cs = map.contour(x,y,wave+mean,15,linewidths=1.5)
    plt.title('contour lines over filled continent background')
    plt.show()


if __name__ == "__main__":
    main()
    sys.exit
    