8459ch06.fm Draft Document for Review December 11, 2019 1:55 pm

vm2_first_ip = "192.168.11.205" # Fist IP from a consecutive pool of IPs vm2_image_name = "xiv_p9_image_rhel76" # The image name vm2_remote_restart = "true" # Enable Auto Remote Restart vm2_storage_name = "xiv_StoragePool" # Storage Template vm2_dockerdisk1 = "64" # Docker disk size in GB for ephemeral storage

- #VM3 configuration (OCP - Workers(App) Nodes) #--------------------------------vm3_number = "2" # Number of VMs vm3_memory = "64" # Memory GB vm3_cpu = "8" # Virtual CPU vm3_vcpu_ratio = "2" # vCPU RATIO 1:2 1 vCPU = 0.5 eCPU (cores) vm3_name = "wrknode" # Hostname prefix vm3_first_ip = "192.168.11.208" # Fist IP from a consecutive pool of IPs vm3_image_name = "xiv_p9_image_rhel76" # The image name vm3_remote_restart = "false" # Disable Auto Remote Restart vm3_storage_name = "xiv_StoragePool" # Storage Template vm3_dockerdisk1 = "128" # Docker disk size in GB for ephemeral storage
- #VM4 configuration (OCP - Load Balancer Node) #--------------------------------vm4_number = "0" # Number of VMs vm4_memory = "8" # Memory GB vm4_cpu = "2" # Virtual CPU vm4_vcpu_ratio = "4" # vCPU RATIO 1:4 1 vCPU = 0.25 eCPU (cores) vm4_name = "lbsnode" # Hostname prefix vm4_first_ip = "192.168.11.212" # Fist IP from a consecutive pool of IPs vm4_image_name = "xiv_p9_image_rhel76" # The image name vm4_remote_restart = "true" # Enable Auto Remote Restart


Attention: To use an existing network, you need to remove the network.tf file before applying the configuration.

Master-Infrastructure and Worker Nodes have an additional disk DOCKER_DISK_1 for docker-vg.

Initialize Terraform working directory:

# cd <PATH> #ocp-aio /ocp-7nodes ocp-3nodes terraform init

Initializing the backend... Initializing provider plugins... The following providers do not have any version constraints in configuration, so the latest version was installed.

... Output truncated

...

- * provider.null: version = "~> 2.1"
- * provider.openstack: version = "~> 1.22" Terraform has been successfully initialized! You may now begin working with Terraform. Try running "terraform plan" to see any changes that are required for your infrastructure. All Terraform commands should now work. If you ever set or change modules or backend configuration for Terraform, rerun this command to reinitialize your working directory. If you forget, other commands will detect it and remind you to do so if necessary.


Create an execution plan:

112 Red Hat OpenShift and IBM Cloud Paks on IBM Power Systems: Volume 1

