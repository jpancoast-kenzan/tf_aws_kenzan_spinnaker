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

import pprint

try:
    import boto.ec2
except ImportError, e:
    print "Missing boto module.  Install with: sudo pip install boto"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit( 2 )

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

'''
{
  "variable": {
    "azs": {
        "description": "AZs per region",
       "default": {
           "us-west-2": "a:b:c"
        }
    },
    "az_counts": {
        "description": "AZ counts per region",
       "default": {
           "us-west-2": "3"
        }
    },
    "all_amis": {
      "description": "The AMI to use",
      "default": {
        "ap-northeast-1-karmic-amd64-pv-instance-store": "ami-2a0fa42b",
        "ap-northeast-1-karmic-i386-pv-instance-store": "ami-240fa425",
        "ap-southeast-1-karmic-amd64-pv-instance-store": "ami-90344ac2"
    }
}
}
}
'''
def main(argv):
    pp = pprint.PrettyPrinter(indent=4)

    variables_file = "variables.tf.json"

    data = {}    
    zone_data = {}
    zone_count_data = {}

    data['variable'] = {}
    data['variable']['azs'] = {}
    data['variable']['az_counts'] = {}
    data['variable']['all_amis'] = {}


    data['variable']['azs']['description'] = "AZs per region"

    data['variable']['az_counts']['description'] = "AZ counts per region"

    data['variable']['all_amis']['description'] = "Ubuntu AMIs"
    


    
    r_ubuntu = requests.get(ubuntu_image_url)

    #The URL actually returns invalid json. 
    ubuntu_good_json = re.sub("],\n]\n}", ']]}', r_ubuntu.text)

    ubuntu_amis = json.loads(ubuntu_good_json)

    '''
    [u'us-gov-west-1', u'trusty', u'14.04 LTS', u'amd64', u'hvm:ebs-io1', u'20151008', u'<a href="https://console.amazonaws-us-gov.com/ec2/home?region=us-gov-west-1#launchAmi=ami-c04725e3">ami-c04725e3</a>', u'hvm']
    
    "ap-southeast-1-karmic-amd64-pv-instance-store": "ami-90344ac2"

    "ap-northeast-1-karmic-amd64-pv-instance-store": "ami-2a0fa42b",
        "ap-northeast-1-karmic-i386-pv-instance-store": "ami-240fa425",
        "ap-southeast-1-karmic-amd64-pv-instance-store": "ami-90344ac2",
        "ap-southeast-1-karmic-i386-pv-instance-store": "ami-e6344ab4",
        "eu-west-1-karmic-amd64-pv-instance-store": "ami-28b9935c",
        "eu-west-1-karmic-i386-pv-instance-store": "ami-24b99350",
        "us-east-1-karmic-amd64-pv-instance-store": "ami-6832d801",
        "us-east-1-karmic-i386-pv-instance-store": "ami-563dd73f",
        "us-west-1-karmic-amd64-pv-instance-store": "ami-0af0a14f",
        "us-west-1-karmic-i386-pv-instance-store": "ami-6ef0a12b",
        "ap-northeast-1-utopic-amd64-hvm-ebs": "ami-6cbca76d",
        "ap-northeast-1-utopic-amd64-hvm-ebs-io1": "ami-7abca77b",
        "ap-northeast-1-utopic-amd64-hvm-ebs-ssd": "ami-80bca781",

        data = Hash[JSON.parse(shit)['aaData'].map { |tuple| ["#{tuple[0]}-#{tuple[1]}-#{tuple[3]}-#{tuple[4].match(/^hvm:/)?'hvm':'pv'}-#{tuple[4].gsub(/^hvm:/, '')}", tuple[6].gsub(/.*>(ami-[^<]*)<.*/, '\1')] }]

    '''

    ami_data = {}

    for ami_info in ubuntu_amis['aaData']:
        ami_id = re.search('/.*>(ami-[^<]*)<.*/', ami_info[6]).group(1)
        key = ami_info[0] + "-" + ami_info[1] + "-" + ami_info[3] + "-"

        if re.match('^hvm', ami_info[4]):
            key +=  "hvm-"
        else:
            key += "pv-"


        key += re.sub('hvm:', '', ami_info[4])

#        print ami_id
#        print key
    
        ami_data[key] = ami_id


    data['variable']['all_amis']['default'] = ami_data
    
    conn = boto.ec2.connect_to_region("us-east-1")

    regions = conn.get_all_regions()


    for region in regions:
        az_string = ''
        zone_count = 0

        temp_conn = boto.ec2.connect_to_region(region.name)

        for zone in temp_conn.get_all_zones():

            az = re.sub(region.name, '', zone.name)
            az_string = az_string + az + ":"

            zone_count += 1

        az_string = re.sub(":$", '', az_string)

        zone_data[region.name] = az_string
        zone_count_data[region.name] = str(zone_count)
    
    data['variable']['azs']['default'] = zone_data
    data['variable']['az_counts']['default'] = zone_count_data


    #data_json = json.dumps(data)
    #print data_json

    f = open(variables_file, 'w')

    f.write(json.dumps(data, indent=4, sort_keys=True))

    f.close()

'''
{
  "variable": {
    "azs": {
        "description": "AZs per region",
       "default": {
           "us-west-2": "a:b:c"
        }
    },
    "az_counts": {
        "description": "AZ counts per region",
       "default": {
           "us-west-2": "3"
        }
    },
    "all_amis": {
      "description": "The AMI to use",
      "default": {
        "ap-northeast-1-karmic-amd64-pv-instance-store": "ami-2a0fa42b",
        "ap-northeast-1-karmic-i386-pv-instance-store": "ami-240fa425",
        "ap-southeast-1-karmic-amd64-pv-instance-store": "ami-90344ac2"
    }
}
}
}
'''

if __name__ == "__main__":
    main(sys.argv)