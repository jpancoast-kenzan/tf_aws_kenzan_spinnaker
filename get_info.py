#!/usr/bin/env python

import sys
#import signal
#import boto.ec2
#import operator
#import getopt
import re
#import yaml
#import os
#import itertools
#import shutil
import boto.ec2

import pprint

try:
    import requests
except ImportError, e:
    print "Missing requests module.  Install with: sudo pip install requests"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit( 2 )

try:
    import json
except ImportError, e:
    print "Missing json module.  Install with: sudo pip install json"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit( 2 )

ubuntu_image_url = "http://cloud-images.ubuntu.com/locator/ec2/releasesTable"

#
#   Shit, some regions only have 2 azs.
#       WTF
#   Wait, I think I've got this handled already, it just rolls over...
#
def main(argv):
    pp = pprint.PrettyPrinter(indent=4)

    '''
    r_ubuntu = requests.get(ubuntu_image_url)

    ubuntu_good_json = re.sub("],\n]\n}", ']]}', r_ubuntu.text)

    print ubuntu_good_json

    ubuntu_amis = json.loads(ubuntu_good_json)

    pp.pprint(ubuntu_amis)
    '''

    conn = boto.ec2.connect_to_region("us-east-1")

    regions = conn.get_all_regions()

    for region in regions:
        print region.name

        temp_conn = boto.ec2.connect_to_region(region.name)

        for zone in temp_conn.get_all_zones():
            print "\t" + zone.name



if __name__ == "__main__":
    main(sys.argv)