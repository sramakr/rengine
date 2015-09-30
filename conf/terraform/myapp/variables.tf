variable "user_name" {}
variable "server_name" {default="test_server2"}
variable "region" { default = "ndc_ch2_e" }
variable "password" {}
variable "image_id" {}
variable "tenant_name" {}
variable "flavor_id" {}
variable "key_pair" {}
variable "auth_url" {
    default = "https://keystone.ece.comcast.net:5000/v2.0"
    }
