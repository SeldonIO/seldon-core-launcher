# Overview

This is the core installer for GCP Launcher. As a user if you wish to install seldon-core on a kubernetes cluster you should follow the docs at https://github.com/SeldonIO/seldon-core. 

If you wish to install and test or develop the core deployer for seldon-core on GCP Launcher then you can follow the instructions below. 

## Create a cluster

```
CLUSTER=cluster-1
ZONE=us-west1-a

# Create the cluster.
gcloud beta container clusters create "$CLUSTER" \
    --zone "$ZONE" \
    --machine-type "n1-standard-1" \
    --num-nodes "3"

# Configure kubectl authorization.
gcloud container clusters get-credentials "$CLUSTER" --zone "$ZONE"

# Bootstrap RBAC cluster-admin for your user.
# More info: https://cloud.google.com/kubernetes-engine/docs/how-to/role-based-access-control
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole cluster-admin --user $(gcloud config get-value account)

# (Optional) Start up kubectl proxy.
kubectl proxy
```

## Setting up GCR

Enable the API:
https://console.cloud.google.com/apis/library/containerregistry.googleapis.com

## Updating git submodules

This repo utilizies git submodules. This repo should typically be included in your
application repo as a submodule as well. Run the following commands to make sure that
all submodules are properly populated. `git clone` does not populate submodules by
default.

```shell
git submodule sync --recursive
git submodule update --recursive --init --force
```

## Development Testing

```
make clean clean_seldon_core
```

Install the CRD (needs to be run just once)

```
make crd/install
```

Install the latest seldon-core using the GCP Deployer image on your cluster.

```
make app/install
```

Install and run a test

```
make app/install-test
```
