# Overview

This is the core installer for GCP Launcher. Depending on your use case you have several ways to install seldon-core on your Kubernetes cluster.

  * For one click installation of seldon core onto a kubernetes cluster use the Google Marketplace UI.
  * As a user if you wish to install seldon-core on a kubernetes cluster you can follow the docs at https://github.com/SeldonIO/seldon-core which has [installation instructions](https://github.com/SeldonIO/seldon-core/blob/master/docs/install.md) using Helm or Ksonnet.
  * If you wish to install, test or develop the core deployer for seldon-core on GCP MarketPlace then you can follow the instructions below which will create seldon-core in the same way as the GCP MarketPlace but using the CLI.

## Create a cluster

Create a kubernetes cluster and ensure you have a cluster-admin role.

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

## Set up GCR

Enable the API:
https://console.cloud.google.com/apis/library/containerregistry.googleapis.com

## Update git submodules

This repo utilizies git submodules. This repo should typically be included in your
application repo as a submodule as well. Run the following commands to make sure that
all submodules are properly populated. `git clone` does not populate submodules by
default.

```shell
git submodule sync --recursive
git submodule update --recursive --init --force
```

## Install Seldon-Core

```
make clean clean_seldon_core
```

Install the CRD (needs to be run just once)

```
make crd/install
```

Setup a service account that has cluster-admin permissions. To create the default service account "seldon", use:

```
export NAMESPACE=default
cat resources/svc_account.yaml | envsubst | kubectl apply -f -
```

Install the latest seldon-core using the GCP Deployer image on your cluster.

```
make app/install
```

Or install and run a test

```
make app/install-test
```

## Configuration

You can configure several parameters via environment variables:

    * NAME : Name of the application
    * NAMESPACE : Namespace to start the application
    * REGISTRY : The Docker registry to use
    * TAG : The image tag to use
    * APIFE_ENABLED : Whether to create the API gateway - should always be true for now
    * APIFE_SVC_TYPE : API Gateway service type, e.g. NodePort or LoadBalancer
    * SVC_ACCOUNT : Service Account to use

For example:

```
export NAMESPACE=seldon
make app/install
```

## Basic Usage

For many example and usage of seldon-core see our main docs at https://github.com/SeldonIO/seldon-core

## Delete

To delete the current app run

```
make app/uninstall
```

Ensure you delete the service account if you created it.

```
cat resources/svc_account.yaml | envsubst | kubectl delete -f -
```



