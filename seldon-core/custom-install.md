# CLI Installation Options

This is the core installer for Google Marketplace. Depending on your use case you have several ways to install seldon-core on your Kubernetes cluster.

  * As a user if you wish to install seldon-core on a kubernetes cluster you can follow the docs at https://github.com/SeldonIO/seldon-core which has [installation instructions](https://github.com/SeldonIO/seldon-core/blob/master/docs/install.md) using Helm or Ksonnet.
  * If you wish to install onto a non-GCP Kubernetes cluster using the same install mechanism that GCP uses or want to customize your install on GCP then you can follow the instructions below:

## Create a cluster

Create a kubernetes cluster and ensure you have a cluster-admin role. The example below is for GCP, but you can use any available cloud or on-premise tool to create your cluster. See the [Kubernetes docs](https://kubernetes.io/docs/setup/) for ways to install Kubernetes.

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

## Set up your Docker Registry

If you are using GCP enable the API:
https://console.cloud.google.com/apis/library/containerregistry.googleapis.com

If you are not using GCP then make sure you set the REGISTRY environment variable below to your Docker registry.

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

For further guides in using seldon-core see our main docs at https://github.com/SeldonIO/seldon-core

## Delete

To delete the current app run

```
make app/uninstall
```

Ensure you delete the service account.

```
make remove_svc_account
```
