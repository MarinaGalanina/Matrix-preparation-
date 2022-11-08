#!/usr/bin/env bash

hubble observe -ojsonpb > output2/hubble_observe_jsonpb.lst

kubectl get pods,replicaset,deployment,daemonset,statefulset,job,cronjob,svc,nodes -A -oyaml > output2/kubernetes_objects.yaml

helm3 ls -A -ojson > output2/helm_ls.json