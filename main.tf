variable "region" {}
variable "distribution" {}
variable "architecture" {
  default = "amd64"
}
variable "virttype" {}
variable "storagetype" {
  default = "instance-store"
}


#{
#  "variable": {
#    "all_amis": {
#      "description": "The AMI to use",
#      "default": {
#        "ap-northeast-1-karmic-amd64-pv-instance-store": "ami-2a0fa42b",
#        "ap-northeast-1-karmic-i386-pv-instance-store": "ami-240fa425",
#        "ap-southeast-1-karmic-amd64-pv-instance-store": "ami-90344ac2",
#

output "ami_id" {
    value = "${lookup(var.all_amis, format(\"%s-%s-%s-%s-%s\", var.region, var.distribution, var.architecture, var.virttype, var.storagetype))}"
}


#{
#	"variable": {
#		"azs": {
#			"description": "AZs per region",
#			"default": {
#				"us-west-2": "a:b:c"
#			}
#		}
#	}
#}

#{
#	"variable": {
#		"az_counts": {
#			"description": "AZ counts per region",
#			"default": {
#				"us-west-2": "3"
#			}
#		}
#	}
#}

output "azs_per_region" {
	value = "${lookup(var.azs, var.region)}"
}

output "az_counts_per_region" {
	value = "${lookup(var.az_counts, var.region)}"
}