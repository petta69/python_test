#!/usr/bin/python36

import sys
import os
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description='Testing testing.')
    parser.add_argument('--test', type=str)

    args = parser.parse_args()


    print ("Hello {}".format(args.test))
    print ("QWE: {}".format(np.__version__))

if __name__ == "__main__":
    main()
    sys.exit
    