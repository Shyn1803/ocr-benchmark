Draft Document for Review December 11, 2019 1:55 pm 8459ch05.fm

## Terraform components are shown in Figure 5-10.

<table>
  <tr>
    <td>![](<b248b19421e4d30d591ae26aadc5850573907db83f2c48d5dc8942d11ef6689b_images/imageFile1.png>)</td>
  </tr>
</table>


Figure 5-10 Terraform components

Configuration files(.tf). Terraform uses its own configuration language, designed to allow concise descriptions of infrastructure. The Terraform language is declarative, describing an intended goal rather than the steps to reach that goal. Terraform binary (executable) file, it is written and compiled in GO language. To install Terraform, find the appropriate package for your system and download it from https://www.terraform.io/downloads.html

Note: Terraform can run on any platform (including x86) to provision resources. If you have a ppc64le platform, you must compile Terraform and all needed providers (plugins). Refer to “Setting up the deployment environment” on page 96.

Terraform state file (.tfstate), a JSON file with running configuration.

# OpenShift-Ansible

Ansible is a simple IT automation engine that automates cloud provisioning, configuration management, application deployment, intra-service orchestration, and many other IT needs.

Chapter 5. Red Hat OpenShift installation planning and considerations 87

