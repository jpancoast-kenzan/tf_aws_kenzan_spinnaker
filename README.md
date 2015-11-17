tf_aws_kenzan_spinnaker
=================

Terraform module to get the current set of publicly available ubuntu AMIs in AWS, the number of AZ's in each aws region, and available AZ's for that region.

This module started off based on https://github.com/terraform-community-modules/tf_aws_ubuntu_ami, everything was re-written in Python and AZ letters and AZ counts were added.

This module grabs all of the AMIs listed at:

    http://cloud-images.ubuntu.com/locator/ec2/

and then looks up the one you want given the input variables

## Input variables

  * region - E.g. eu-central-1
  * distribution - E.g. trusty
  * architecture - amd64/i386
  * virttype - hvm/pv
  * storagetype - instance-store/ebs-io1/ebs-ssd/ebs

## Outputs

  * ami_id
  * azs_per_region
  * az_counts_per_region

## Example use

    module "tf_aws_kenzan_spinnaker" {
      source = "github.com/kenzanlabs/tf_aws_kenzan_spinnaker"
      region = "${var.region}"
      distribution = "trusty"
      architecture = "amd64"
      virttype = "hvm"
      storagetype = "ebs-ssd"
    }

    resource "aws_instance" "web" {
      ami = "${module.tf_aws_kenzan_spinnaker.ami_id}"
      instance_type = "m3.8xlarge"
    }

    availability_zone    = "${var.region}${element(split (":", "${module.tf_aws_kenzan_spinnaker.azs_per_region}"), count.index%module.tf_aws_kenzan_spinnaker.az_counts_per_region)}"

Apache2 - see the included LICENSE file for more details.

