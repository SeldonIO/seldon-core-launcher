# Seldon Release Process

Internal Seldon release process.
 1. Start a new Kubernetes cluster in launcher-testing project
 1. ```make crd/install```
 1. Update TAG and PULL_TAG in Makefile
    1. TAG is Google track
    1. PULL_TAG is seldon-core release
 1. ```make clean clean_seldon_core```
 1. Set project to `launcher-testing` project, e.g. ```gcloud config configurations activate gcp-launcher-testing``` 
 1. ```make app/install-test```
    1. Check logs `kubectl logs pod/seldon-core-1-tester` to see if ends with SUCCESS
 1. Delete kubernetes cluster
 1. commit and push changes to project
 1. If ok, then set project to `seldon-core-public` project e.g., ```gcloud config configurations activate seldon-core-public```
 1. ```make clean clean_seldon_core``` 
 1. ```make app/build```