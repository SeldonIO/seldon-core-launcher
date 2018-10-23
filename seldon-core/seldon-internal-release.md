# Seldon Release Process

Internal Seldon release process.

 1. Update TAG and PULL_TAG in Makefile
    1. TAG is Googl track
    1. PULL_TAG is seldon-core release
 1. ```make clean clean_seldon_core```
 1. Set project to testing project ```gcloud config configurations activate gcp-launcher-testing```
 1. ```make app/install-test```
 1. If ok, then ```gcloud config configurations activate seldon-core-public```
 1. ```make clean clean_seldon_core``` 
 1. ```make app/build```