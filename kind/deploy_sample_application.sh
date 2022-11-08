#!/usr/bin/env bash

for namespace in namespace-a namespace-b namespace-c; do
  kubectl create namespace ${namespace}
done

for namespace in namespace-a namespace-b namespace-c; do
  helm3 install -n ${namespace} echo csf-stable/compaas-echoserver-test
done

kubectl apply -f restrict-namespace-c.yaml
