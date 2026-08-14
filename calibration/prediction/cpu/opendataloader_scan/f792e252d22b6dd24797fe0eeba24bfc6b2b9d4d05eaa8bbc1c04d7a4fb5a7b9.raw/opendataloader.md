environment. The Master, Infrastructure and Compute Roles are deployed to a single node (Figure 6-1).

![](<f792e252d22b6dd24797fe0eeba24bfc6b2b9d4d05eaa8bbc1c04d7a4fb5a7b9_images/imageFile1.png>)

Automation

Application

Cluster

Administrators   Developers

CVCD Tools

Owners

Web Console :8443

Router :80 & :443

2

https:llocp example.com:8443

Application Users

REGISTRY

https J<myapp>.ocp.example.com:443

Jenkins

POD

POD

POD

POD

POD

POD

3

Prometheus

PODs

K8s Operators

OLM

PVC Storage

Figure 6-1 OpenShift Container Platform 3.11 all-in-one

Seven nodes deployment is highly available and suitable for production. The Master and Infrastructure Roles are deployed to three Nodes, the Computer Role is deployed to three Worker Nodes, and the Load Balancer is deployed to a single Node (Figure 6-2).

![](<f792e252d22b6dd24797fe0eeba24bfc6b2b9d4d05eaa8bbc1c04d7a4fb5a7b9_images/imageFile2.png>)

https J<myapp>.ocp.example.com:443

Application

Automation

Cluster

Aplication

CVCD Tools

Administrators

Developers

Owners

Users

Load Balancer [LB]

App

App

App

POD

POD

POD

POD

Routters

Master

Intra

Master

Intra

Master

Intra

Registry

PVC Storage

Application Nodes

Master Nodes

Figure 6-2 OpenShift Container Platform 3.11 6xNodes + Load Balancer

