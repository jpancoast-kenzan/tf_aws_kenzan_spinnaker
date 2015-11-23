tf_aws_kenzan_spinnaker
=================

Terraform module to get the current set of publicly available ubuntu AMIs in AWS, the publically available Spinnaker AMIs, the number of AZ's in each aws region, and available AZ's for that region. Designed to be used with https://github.com/kenzanlabs/spinnaker-terraform

This module started off based on https://github.com/terraform-community-modules/tf_aws_ubuntu_ami, everything was re-written in Python and AZ letters and AZ counts were added.

This module grabs all of the Ubuntu AMIs listed at:

    http://cloud-images.ubuntu.com/locator/ec2/

and then looks up the one you want given the input variables

It also grabs all the Spinnaker AMIs listed at:

    https://raw.githubusercontent.com/spinnaker/spinnaker.github.io/master/online_docs/quick_ref/ami_table.md

    
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
  * Kenzan Produced Spinnaker AMI's

## Example use

    module "tf_aws_kenzan_spinnaker" {
      source = "github.com/kenzanlabs/tf_aws_kenzan_spinnaker"
      region = "${var.region}"
      distribution = "trusty"
      architecture = "amd64"
      virttype = "hvm"
      storagetype = "ebs-ssd"
    }

    resource "aws_instance" "ubuntu" {
      ami = "${module.tf_aws_kenzan_spinnaker.ami_id}"
      instance_type = "m3.8xlarge"
    }

    resource "aws_instance" "spinnaker" {
      ami = "${module.tf_aws_kenzan_spinnaker.spinnaker_ami_id}"
      instance_type = "m3.8xlarge"
    }

    availability_zone    = "${var.region}${element(split (":", "${module.tf_aws_kenzan_spinnaker.azs_per_region}"), count.index%module.tf_aws_kenzan_spinnaker.az_counts_per_region)}"

Apache2 - see the included LICENSE file for more details.

