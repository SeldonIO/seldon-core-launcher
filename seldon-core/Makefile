#TAG ?= latest
TAG ?= 0.2.1-SNAPSHOT-CRD

# crd.Makefile provides targets to install Application CRD.
include ../vendor/marketplace-tools/crd.Makefile

# gcloud.Makefile provides default values for
# REGISTRY and NAMESPACE derived from local
# gcloud and kubectl environments.
include ../vendor/marketplace-tools/gcloud.Makefile

# marketplace.Makefile provides targets such as
# ".build/marketplace/deployer/envsubst" to build the base
# deployer images locally.
include ../vendor/marketplace-tools/marketplace.Makefile

# ubbagent.Makefile provides ".build/ubbagent/ubbagent"
# target to build the ubbagent image locally.
include ../vendor/marketplace-tools/ubbagent.Makefile
include ../vendor/marketplace-tools/var.Makefile

# app.Makefile provides the main targets for installing the
# application.
# It requires several APP_* variables defined as followed.
include ../vendor/marketplace-tools/app.Makefile

APP_DEPLOYER_IMAGE ?= $(REGISTRY)/seldonio/seldon-core/deployer:$(TAG)
NAME ?= seldon-core-1
APP_PARAMETERS ?= { \
  "name": "$(NAME)", \
  "namespace": "$(NAMESPACE)", \
  "cluster_manager.image.name": "$(REGISTRY)/seldonio/seldon-core/cluster-manager:$(TAG)", \
  "engine.image.name": "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)", \
  "apife.enabled": "true", \
  "apife.image.name": "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)", \
  "redis.image.name": "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)", \
  "rbac.service_account.name": "seldon", \
  "rbac.service_account.create": "false", \
  "application.enabled": "true" \
}
TESTER_IMAGE ?= $(REGISTRY)/example/seldon-core/tester:$(TAG)
APP_TEST_PARAMETERS ?= { \
  "tester.image": "$(TESTER_IMAGE)" \
}

app/install::
	kubectl apply -f apptest/sa.yaml

# Extend the target as defined in app.Makefile to
# include real dependencies.
app/build:: .build/seldon-core/deployer \
            .build/seldon-core/cluster-manager \
            .build/seldon-core/engine \
            .build/seldon-core/apife \
            .build/seldon-core/redis \
            .build/seldon-core/tester \
            .build/seldon-core/updated_helm_values

seldon-core: 
	git clone -b crd_create https://github.com/cliveseldon/seldon-core.git

.build/seldon-core: | .build
	mkdir -p "$@"

.build/seldon-core/updated_helm_values: .build/seldon-core seldon-core
	$(call print_target, $@)
	python update_helm_chart.py
	@touch "$@"

.build/seldon-core/deployer: apptest/deployer/* \
                       apptest/deployer/seldon-core/* \
                       apptest/deployer/seldon-core/templates/* \
                       deployer/* \
		       .build/seldon-core/updated_helm_values \
                       schema.yaml \
                       .build/marketplace/deployer/helm \
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
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/cluster-manager:$(TAG)
	docker tag seldonio/cluster-manager:$(TAG) "$(REGISTRY)/seldonio/seldon-core:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core:$(TAG)"
	@touch "$@"

# Simulate building of engine. Actually just copying public image to
# local registry.
.build/seldon-core/engine: .build/var/REGISTRY \
                    .build/var/TAG \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/engine:$(TAG)
	docker tag seldonio/engine:$(TAG) "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/engine:$(TAG)"
	@touch "$@"

# Simulate building of apife. Actually just copying public image to
# local registry.
.build/seldon-core/apife: .build/var/REGISTRY \
                    .build/var/TAG \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull seldonio/apife:$(TAG)
	docker tag seldonio/apife:$(TAG) "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/apife:$(TAG)"
	@touch "$@"

# Simulate building of apife. Actually just copying public image to
# local registry.
.build/seldon-core/redis: .build/var/REGISTRY \
                    .build/var/TAG \
                    | .build/seldon-core
	$(call print_target, $@)
	docker pull redis:4.0.1
	docker tag redis:4.0.1 "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)"
	docker push "$(REGISTRY)/seldonio/seldon-core/redis:$(TAG)"
	@touch "$@"


.PHONY: clean
clean_seldon_core:
	rm -rf seldon-core
	rm -f .build/seldon-core/updated_helm_values
