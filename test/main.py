import kopf
import kubernetes as k8s

RESOURCE_GROUP = "nokia.org"
RESOURCE_VERSION = "v1"
RESOURCE_TYPE = "testenv"

@kopf.on.create(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def create_custom_resource(body, spec , logger, **kwargs):
    name= body["metadata"]["name"]
    host_user= spec["hostUser"]
    service_port=spec["port"]

