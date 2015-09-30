resource "openstack_compute_instance_v2" "test_server2" {
  name = "tf-test3"
  region = "${var.region}"
  image_id = "${var.image_id}"
  flavor_id = "${var.flavor_id}"
  metadata {
  	this = "that"
	}
  key_pair = "${var.key_pair}"
  security_groups = ["daas_ssh"]
  }

output "ip" {
    value = "${openstack_compute_instance_v2.test_server2.access_ip_v4}"
}
