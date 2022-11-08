import typing
import yaml
import os


class KubernetesObject:

    def __init__(self, parent=None, name=None, namespace=None, kind=None):
        self.myself: str = name
        self.parent: KubernetesObject = parent
        self.name: str = name
        self.namespace: str = namespace
        self.kind: str = kind

    def get_top_parent(self, kubernetes_store):
        parent_object = self
        while hasattr(parent_object, f'ownerReferences'):
            current_object = kubernetes_store.find_object(kind=parent_object.ownerReferences[0]["kind"],
                                                          name=parent_object.ownerReferences[0]["name"],
                                                          namespace=parent_object.namespace)

            parent_object = current_object

        return parent_object

    def add_attribute(self, name, val):
        setattr(self, f'{name}', val)

    def __repr__(self):
        return f'KubernetesObject(name="{self.name}",namespace="{self.namespace}",kind="{self.kind}")'


class KubernetesStore:

    def __init__(self, filename: str):
        self.kubernetes_objects_list = self._load(filename)

    def _load(self, filename: str) -> typing.List[KubernetesObject]:
        print(f'KubernetesStore import file in yaml format:{filename}')
        classes = []
        if os.path.isfile(filename):
            with open(filename, 'r') as yaml_file:
                configuration = yaml.safe_load(yaml_file)
                for data in configuration['items']:
                    items = KubernetesObject(name='items', parent=None)
                    self._yaml_to_classes(data, items)
                    classes.append(items)
            return classes
        else:
            print('File kubernetes doesnt exists')
        return classes

    def _yaml_to_classes(self, nested_dictionary: dict, parent: KubernetesObject):
        for key, value in nested_dictionary.items():
            keys = f'{key}'
            if type(value) is dict:
                obj = KubernetesObject(name=keys, parent=parent)
                if parent.kind:
                    obj.kind = parent.kind
                parent.add_attribute(key, obj)
                self._yaml_to_classes(value, obj)

            else:
                parent.add_attribute(keys, value)

    def find_object(self, kind: str, name: str, namespace: str):

        for kubernetes_find_object in self.kubernetes_objects_list:
            if kubernetes_find_object.kind == kind and kubernetes_find_object.metadata.name == name and kubernetes_find_object.metadata.namespace == namespace:
                return kubernetes_find_object.metadata
        return None

    def find_pod(self, name: str, namespace: str) -> KubernetesObject:

        for kubernetes_object in self.kubernetes_objects_list:
            if kubernetes_object.kind == f"Pod" and hasattr(kubernetes_object.metadata, f'generateName'):
                if kubernetes_object.metadata.name == name:
                    return kubernetes_object.metadata
        return None
