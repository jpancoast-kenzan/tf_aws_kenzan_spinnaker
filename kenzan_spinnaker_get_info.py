#!/usr/bin/env python

import sys
import re
import pprint
import os

try:
    import boto.ec2
except ImportError, e:
    print "Missing boto module.  Install with: sudo pip install boto"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit(2)

try:
    import requests
except ImportError, e:
    print "Missing requests module.  Install with: sudo pip install requests"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit(2)

try:
    import json
except ImportError, e:
    print "Missing json module.  Install with: sudo pip install json"
    print "If you don't have pip, do this first: sudo easy_install pip"
    exit(2)

ubuntu_image_url = "http://cloud-images.ubuntu.com/locator/ec2/releasesTable"


def main(argv):
    pp = pprint.PrettyPrinter(indent=4)

    variables_file = "variables.tf.json"

    data_error = False

    data = {}
    zone_data = {}
    zone_count_data = {}
    ami_data = {}

    data['variable'] = {}
    data['variable']['azs'] = {}
    data['variable']['az_counts'] = {}
    data['variable']['all_amis'] = {}

    data['variable']['azs']['description'] = "AZs per region"
    data['variable']['az_counts']['description'] = "AZ counts per region"
    data['variable']['all_amis']['description'] = "Ubuntu AMIs"

    r_ubuntu = requests.get(ubuntu_image_url)

    aws_conn = boto.ec2.connect_to_region("us-east-1")

    regions = aws_conn.get_all_regions()

    # The URL actually returns invalid json.
    ubuntu_good_json = re.sub("],\n]\n}", ']]}', r_ubuntu.text)

    ubuntu_amis = json.loads(ubuntu_good_json)

    for ami_info in ubuntu_amis['aaData']:
        ami_id = re.search('/.*>(ami-[^<]*)<.*/', ami_info[6]).group(1)
        key = ami_info[0] + "-" + ami_info[1] + "-" + ami_info[3] + "-"

        if re.match('^hvm', ami_info[4]):
            key += "hvm-"
        else:
            key += "pv-"

        key += re.sub('hvm:', '', ami_info[4])

        ami_data[key] = ami_id

    data['variable']['all_amis']['default'] = ami_data

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

    '''
    Check to make sure all parts have some data in them
    
    Things to check:
        data['variable']['az_counts']['default'] has more than 1 entry
        data['variable']['azs']['default'] has more than 1 entry
        data['variable']['all_amis']['default']
    '''
    if len(data['variable']['az_counts']['default'].keys()) < 1 or \
            len(data['variable']['azs']['default'].keys()) < 1:

        print "WARNING: NO AZ DATA"
        data_error = True

    if len(data['variable']['all_amis']['default'].keys()) < 1:
        print "WARNING: NO AMI DATA"
        data_error = True

    if data_error:
        if os.path.isfile(variables_file):
            # exit status 1 means there was a data error, but the variables
            # file exists, so it's probably OK to continue.
            sys.exit(1)
        else:
            # exit status 2 means there was a data error AND the variables file
            # DOES NOT EXIST, so it is NOT OK to continue
            sys.exit(2)

    f = open(variables_file, 'w')

    f.write(json.dumps(data, indent=4, sort_keys=True))

    f.close()


if __name__ == "__main__":
    main(sys.argv)
