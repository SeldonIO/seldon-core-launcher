# Overview

Seldon-Core provides machine learning deployment for Kubernetes.

 - Allows data scientists to create models using any machine learning toolkit or programming language. We plan to initially cover the tools/languages below:
   - Python based models including
     - Tensorflow models
     - Sklearn models
   - Spark models
   - H2O models
   - R models
 - Exposes machine learning models via REST and gRPC automatically when deployed for easy integration into business apps that need predictions.
 - Allows complex runtime inference graphs to be deployed as microservices. These graphs can be composed of:
   - Models - runtime inference executable for machine learning models
   - Routers - route API requests to sub-graphs. Examples: AB Tests, Multi-Armed Bandits.
   - Combiners - combine the responses from sub-graphs. Examples: ensembles of models
   - Transformers - transform request or responses. Example: transform feature requests.
 - Handles full lifecycle management of the deployed model:
    - Updating the runtime graph with no downtime
    - Scaling
    - Monitoring

# Installation

## Quick Install - FIXME

## Command line instructions

### Prerequisites

- Setup cluster
  - Permissions
- Setup kubectl
- Setup helm
- Install Application Resource

### Commands

Set environment variables (modify if necessary):
```
export APP_INSTANCE_NAME=seldon-1
export NAMESPACE=default
```

Expand manifest template:
```
helm template . --set APP_INSTANCE_NAME=$APP_INSTANCE_NAME,NAMESPACE=$NAMESPACE > expanded.yaml
```

Run kubectl:
```
kubectl apply -f expanded.yaml
```
