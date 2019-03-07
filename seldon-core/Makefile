TAG ?= 0.2
PULL_TAG ?= 0.2.6

##### crd.Makefile provides targets to install Application CRD.
####include ../vendor/marketplace-tools/crd.Makefile
####
##### gcloud.Makefile provides default values for
##### REGISTRY and NAMESPACE derived from local
##### gcloud and kubectl environments.
####include ../vendor/marketplace-tools/gcloud.Makefile
####
##### marketplace.Makefile provides targets such as
##### ".build/marketplace/deployer/envsubst" to build the base
##### deployer images locally.
####include ../vendor/marketplace-tools/marketplace.Makefile
####
##### ubbagent.Makefile provides ".build/ubbagent/ubbagent"
##### target to build the ubbagent image locally.
####include ../vendor/marketplace-tools/ubbagent.Makefile
####include ../vendor/marketplace-tools/var.Makefile
####
##### app.Makefile provides the main targets for installing the
##### application.
##### It requires several APP_* variables defined as followed.
####include ../vendor/marketplace-tools/app.Makefile

# Convenience makefiles.
include ../gcloud.Makefile
include ../var.Makefile

# app.Makefile provides the main targets for installing the
# application.
# It requires several APP_* variables defined as followed.
include ../app.Makefile

#### Not included in example
include ../crd.Makefile


###include ../vendor/marketplace-tools/common.Makefile
###include ../vendor/marketplace-tools/crd.Makefile
###include ../vendor/marketplace-tools/gcloud.Makefile
###include ../vendor/marketplace-tools/marketplace.Makefile
###include ../vendor/marketplace-tools/var.Makefile

APP_DEPLOYER_IMAGE ?= $(REGISTRY)/seldonio/seldon-core/deployer:$(TAG)
NAME ?= seldon-core-1
APIFE_ENABLED ?= true
APIFE_SVC_TYPE ?= NodePort
SVC_ACCOUNT ?= seldon
APP_PARAMETERS ?= { \
  "name": "$(NAME)", \
  "namespace": "$(NAMESPACE)", \
  "cluster_manager.image.name": "$(REGISTRY)/seldonio/seldon-core:$(TAG)", \
  "engine.image.name": "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)", \
  "apife.enabled": "$(APIFE_ENABLED)", \
  "apife.service_type": "$(APIFE_SVC_TYPE)", \
  "apife.image.name": "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)", \
  "redis.image.name": "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)", \
  "rbac.service_account.name": "$(SVC_ACCOUNT)" \
}
TESTER_IMAGE ?= $(REGISTRY)/example/seldon-core/tester:$(TAG)
APP_TEST_PARAMETERS ?= { \
  "tester.image": "$(TESTER_IMAGE)" \
}

.PHONY: remove_svc_account
remove_svc_account:
	export NAMESPACE=${NAMESPACE} && cat resources/svc_account.yaml | envsubst | kubectl delete -f -

.PHONY: create_svc_account
create_svc_account:
	export NAMESPACE=${NAMESPACE} && cat resources/svc_account.yaml | envsubst | kubectl apply -f -

app/install:: create_svc_account

app/install-test:: create_svc_account

# Extend the target as defined in app.Makefile to
# include real dependencies.
app/build:: .build/seldon-core/deployer \
            .build/seldon-core/cluster-manager \
            .build/seldon-core/engine \
            .build/seldon-core/apife \
            .build/seldon-core/redis \
            .build/seldon-core/tester \
            .build/seldon-core/updated_helm_values

#FIXME set release branch to clone from when dev stage os over
seldon-core: 
	git clone https://github.com/SeldonIO/seldon-core.git

.build/seldon-core: | .build
	mkdir -p "$@"

seldon-core/helm-charts/seldon-core/templates/application.yaml: seldon-core
	cp resources/application.yaml seldon-core/helm-charts/seldon-core/templates/application.yaml

.build/seldon-core/updated_helm_values: | .build/seldon-core seldon-core seldon-core/helm-charts/seldon-core/templates/application.yaml
	$(call print_target, $@)
	python scripts/update_helm_chart.py
	@touch "$@"

.build/seldon-core/deployer: apptest/deployer/* \
                       apptest/deployer/seldon-core/* \
                       apptest/deployer/seldon-core/templates/* \
                       deployer/* \
		       .build/seldon-core/updated_helm_values \
                       schema.yaml \
			seldon-core \
                       .build/var/APP_DEPLOYER_IMAGE \
                       .build/var/REGISTRY \
                       .build/var/TAG \
                       | .build/seldon-core/cluster-manager
	$(call print_target, $@)
	docker build \
	    --build-arg REGISTRY="$(REGISTRY)" \
	    --build-arg TAG="$(TAG)" \
	    --tag "$(APP_DEPLOYER_IMAGE)" \
	    -f deployer/Dockerfile \
	    .
	docker push "$(APP_DEPLOYER_IMAGE)"
	@touch "$@"


.build/seldon-core/tester:
	$(call print_target, $@)
	docker pull cfmanteiga/alpine-bash-curl-jq
	docker tag cfmanteiga/alpine-bash-curl-jq "$(TESTER_IMAGE)"
	docker push "$(TESTER_IMAGE)"
	@touch "$@"


# Simulate building of cluster-manager. Actually just copying public image to
# local registry.
.build/seldon-core/cluster-manager: .build/var/REGISTRY \
                    .build/var/TAG \
                    .build/seldon-core/updated_helm_values \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/cluster-manager:$(PULL_TAG)
	docker tag seldonio/cluster-manager:$(PULL_TAG) "$(REGISTRY)/seldonio/seldon-core:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core:$(TAG)"
	@touch "$@"

# Simulate building of engine. Actually just copying public image to
# local registry.
.build/seldon-core/engine: .build/var/REGISTRY \
                    .build/var/TAG \
		    .build/seldon-core/updated_helm_values \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/engine:$(PULL_TAG)
	docker tag seldonio/engine:$(PULL_TAG) "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)"
	@touch "$@"

# Simulate building of apife. Actually just copying public image to
# local registry.
.build/seldon-core/apife: .build/var/REGISTRY \
                    .build/var/TAG \
                    .build/seldon-core/updated_helm_values \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/apife:$(PULL_TAG)
	docker tag seldonio/apife:$(PULL_TAG) "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)"
	@touch "$@"

# Simulate building of redis. Actually just copying public image to
# local registry.
.build/seldon-core/redis: .build/var/REGISTRY \
                    .build/var/TAG \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull launcher.gcr.io/google/redis4:4.0
	docker tag launcher.gcr.io/google/redis4:4.0 "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)"
	@touch "$@"


.PHONY: clean
clean_seldon_core:
	rm -rf seldon-core
	rm -f .build/seldon-core/updated_helm_values
