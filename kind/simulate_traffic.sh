#!/usr/bin/env bash

for namespace in namespace-a namespace-b namespace-c; do
  pod_name=$(kubectl get pod -n${namespace} -lapp=compaas-echoserver-test,release=echo -ojsonpath='{.items[0].metadata.name}')
  for dst in echo-compaas-echoserver-test.namespace-a.svc \
             echo-compaas-echoserver-test.namespace-b.svc \
             echo-compaas-echoserver-test.namespace-c.svc \
             api.twitter.com; do
    echo "Run traffic from ${namespace} (${pod_name}) to ${dst}"
    kubectl exec -it ${pod_name} -n${namespace} -- curl -ksI --connect-timeout 10 https://${dst}
  done
done