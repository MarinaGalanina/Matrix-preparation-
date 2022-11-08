import typing
import argparse
import sys
from models.component import Component
from store.hubble_store import HubbleStore, ConnectionPeer
from store.helm_store import HelmStore, HelmRelease
from store.kubernetes_store import KubernetesStore, KubernetesObject
from utilities.logger import *
import json

logger.debug('Debug message')
logger.info('Level message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical-level message')


def map_to_pod(connection_peer: ConnectionPeer, kubernetes_store: KubernetesStore) -> KubernetesObject:
    if 'pod_name' in connection_peer and 'namespace' in connection_peer:
        return kubernetes_store.find_pod(connection_peer['pod_name'], connection_peer['namespace'])
    return None


def map_to_release(top_object: KubernetesObject, helm_store: HelmStore) -> HelmRelease:
    for helm in helm_store.helm_releases_list:
        if hasattr(top_object.annotations, f'meta.helm.sh/release-namespace') and (
                top_object.annotations, f'meta.helm.sh/release-name'):
            if helm.namespace == getattr(top_object.annotations,
                                         'meta.helm.sh/release-namespace') and helm.name == getattr(
                top_object.annotations, 'meta.helm.sh/release-name'):
                return helm

    return None


def map_to_component(connection_peer: ConnectionPeer,
                     kubernetes_store: KubernetesStore,
                     helm_store: HelmStore,
                     components: typing.List[Component]):
    pod = map_to_pod(connection_peer, kubernetes_store)
    logger.debug(f'Connection peer map to pod {pod}')
    if pod:
        top_object = pod.get_top_parent(kubernetes_store)
        logger.debug(f'Top object is {top_object.__dict__}')
        helm_release = map_to_release(top_object, helm_store)

        logger.debug(f'Object is map to release{helm_release}')
        if helm_release is not None:
            for component in components:
                #component.update_services(helm_release)
                logger.debug(f'Component is in components list')
                if component.release == helm_release.name:
                    component.update_services(top_object)
                    logger.debug(f'Component release is the same as helm release:{component.release} ')

                    return component


def helm_releases_to_components(helm_store: HelmStore) -> typing.List[Component]:
    list_of_components = []
    for helm in helm_store.helm_releases_list:
        helm_components = Component(name=helm.name, namespace=helm.namespace, description=helm.chart)
        list_of_components.append(helm_components)
    return list_of_components


def main(args):
    hubble_store = HubbleStore(args.hubble_connections_file)
    helm_store = HelmStore(args.helm_releases_file)
    kubernetes_store = KubernetesStore(args.kubernetes_objects_file)
    components = helm_releases_to_components(helm_store)

    for connection in hubble_store.connections_list:
        destination_component = map_to_component(connection.destination, kubernetes_store, helm_store, components)
        source_component = map_to_component(connection.source, kubernetes_store, helm_store, components)
        if source_component:
            source_component.update_transfer_leyer(connection.flow.l4)
            source_component.update_portID(connection.flow.l4)
            source_component.update_connections(connection.source)
        if destination_component:
            destination_component.update_transfer_leyer(connection.flow.l4)
            destination_component.update_portID(connection.flow.l4)
            destination_component.update_ports(connection.destination)


# print(f"{len(components)=}")
        components[0].dump_to_file(args.output_dir)


def parseArguments():
    SCRIPT_NAME = sys.argv[0]
    description = f"""Generates connection matrix in common format based on hubble/kubernetes/helm input files.

Example call:
{SCRIPT_NAME} -i time.txt
"""

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description)
    parser.add_argument('--hubbleConnectionsFile', dest="hubble_connections_file", required=True,
                        help='Connection file from Hubble. Each line contains connection in json format.')
    parser.add_argument('--kubernetesObjectsFile', dest="kubernetes_objects_file", required=True,
                        help='Kubernetes objects file. File in yaml format, contains objects in items key.')
    parser.add_argument('--helmReleasesFile', dest="helm_releases_file", required=True,
                        help='Input connection file from Hubble. Each line contains connection in json format.')
    parser.add_argument('--outputDir', dest="output_dir", required=True,
                        help='Output directory for generated components in a common format.')
    parser.add_argument('-v', '--verbose', help='Enable verbose output.', action="store_true", default=False)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parseArguments()
    VERBOSE = args.verbose
    sys.exit(main(args))
