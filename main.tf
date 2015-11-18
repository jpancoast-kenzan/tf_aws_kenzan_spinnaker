variable "region" {}
variable "distribution" {}
variable "architecture" {
  default = "amd64"
}
variable "virttype" {}
variable "storagetype" {
  default = "instance-store"
}

output "ami_id" {
    value = "${lookup(var.all_amis, format(\"%s-%s-%s-%s-%s\", var.region, var.distribution, var.architecture, var.virttype, var.storagetype))}"
}

output "spinnaker_ami_id" {
	value = "${lookup(var.spinnaker_amis, format(\"%s-%s\", var.region, var.virttype))}"
}

output "azs_per_region" {
	value = "${lookup(var.azs, var.region)}"
}

output "az_counts_per_region" {
	value = "${lookup(var.az_counts, var.region)}"
}