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


<<<<<<< HEAD
    print "Hello {}".format(args.test)
    print "Pietro: {}".format(np.__version__)
=======
    print "Peter {}".format(args.test)
    print "QWE: {}".format(np.__version__)
>>>>>>> hemma_test

    map = Basemap(projection='cyl',llcrnrlon=0,llcrnrlat=50, urcrnrlon=30, urcrnrlat=75,resolution='l')#,
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='coral',lake_color='blue')
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='aqua')
    # draw lat/lon grid lines every 30 degrees.
    map.drawmeridians(np.arange(0,360,10))
    map.drawparallels(np.arange(-90,90,10))
    #cs = map.contour(x,y,wave+mean,15,linewidths=1.5)
    plt.title('contour lines over filled continent background')
    plt.show()


if __name__ == "__main__":
    main()
    sys.exit
    