![seldon](./seldon.png)

Welcome to Seldon-Core. Machine learning deployment on Kubernetes.

Its high level goals are:


 - Allow data scientists to create models using any machine learning toolkit or programming language. We plan to initially cover the tools/languages below:
   - Python based models including
     - Tensorflow models
     - Sklearn models
   - Spark models
   - H2O models
   - R models
 - Expose machine learning models via REST and gRPC automatically when deployed for easy integration into business apps that need predictions.
 - Allow complex runtime inference graphs to be deployed as microservices. These graphs can be composed of:
   - Models - runtime inference executable for machine learning models
   - Routers - route API requests to sub-graphs. Examples: AB Tests, Multi-Armed Bandits.
   - Combiners - combine the responses from sub-graphs. Examples: ensembles of models
   - Transformers - transform request or responses. Example: transform feature requests.
 - Handle full lifecycle management of the deployed model:
    - Updating the runtime graph with no downtime
    - Scaling
    - Monitoring
    - Security

# Getting Started

If you have just installed Seldon via the Google Marketplace you can jump straight away to our getting started notebooks:

 * [Deploy a pre-built model with seldon-core](./getting_started/deployment/deploy.ipynb)
   * This notebook will take you through deploying a model and then an AB test between two models. You will serve requests using REST and gRPC endpoints.
 * [Wrap a model and deploy under seldon-core](./getting_started/wrap-model/wrap_model.ipynb)
   * This notebook will show how you can build yourown models and deploy runtime inference code onto seldon-core.


# Further Steps

You can read more detailed [getting started docs](https://github.com/SeldonIO/seldon-core/blob/master/docs/getting_started/readme.md) in the central [seldon-core project](https://github.com/SeldonIO/seldon-core).


If you wish to install Seldon from the command line using the same tools as the Marketplace UI uses you can view the docs [here](custom-install.md).




