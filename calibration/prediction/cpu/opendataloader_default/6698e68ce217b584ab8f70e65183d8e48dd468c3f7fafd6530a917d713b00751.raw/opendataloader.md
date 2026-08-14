8459ch06.fm Draft Document for Review December 11, 2019 1:55 pm

- • Compile OpenStack plugin for the ppc64le platform:
- • Compile Null plugin for the ppc64le platform:


### mkdir -p $GOPATH/src/github.com/terraform-providers; cd $GOPATH/src/github.com/terraform-providers git clone https://github.com/terraform-providers/terraform-provider-openstack

Cloning into 'terraform-provider-openstack'... remote: Enumerating objects: 189, done. remote: Counting objects: 100% (189/189), done. remote: Compressing objects: 100% (163/163), done. remote: Total 17434 (delta 59), reused 101 (delta 21), pack-reused 17245 Receiving objects: 100% (17434/17434), 11.96 MiB | 1.54 MiB/s, done. Resolving deltas: 100% (10138/10138), done.

### cd $GOPATH/src/github.com/terraform-providers/terraform-provider-openstack git checkout v1.22.0

Note: checking out 'v1.22.0'.

... Output truncated

...

### HEAD is now at 7dcd493... v1.22.0 XC_OS=linux XC_ARCH=ppc64le make build

==> Checking that code complies with gofmt requirements... go install

mkdir -p $GOPATH/src/github.com/terraform-providers ; cd $GOPATH/src/github.com/terraform-providers/ git clone https://github.com/terraform-providers/terraform-provider-null.git

Cloning into 'terraform-provider-null'...

... Output truncated

... Resolving deltas: 100% (2057/2057), done.

cd $GOPATH/src/github.com/terraform-providers/terraform-provider-null git checkout v2.1.2

Note: checking out 'v2.1.2'.

... Output truncated

...

### HEAD is now at 8d3d85a... v2.1.2 XC_OS=linux XC_ARCH=ppc64le make build

==> Checking that code complies with gofmt requirements... go install

# 6.3 OpenShift container platform deployment

This section provides an OpenShift container deployment platform.

## 6.3.1 Deployment scenarios

This section presents the most common scenarios that can be used to start deploying OpenShift clusters:

Single node deployment (all-in-one) is not an officially supported OpenShift deployment. The all-in-one (AIO) configuration is considered a testing or development

104 Red Hat OpenShift and IBM Cloud Paks on IBM Power Systems: Volume 1

