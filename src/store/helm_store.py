import typing
import json
import os

class HelmRelease:
    def __init__(self, parent=None, name=None,namespace=None):
        self.myself: str = name
        self.parent: HelmRelease = parent
        self.name: str = name
        self.namespace: str = namespace

    def get_top_parent(self):
        return self.parent

    def add_attribute(self, name, val):
        setattr(self, f'{name}', val)

    def __repr__(self):
        return f'HelmRelease(name="{self.name}",namespace={self.namespace}")'

class HelmStore:

    def __init__(self, filename: str):
        self.helm_releases_list = self._load(filename)

    def _load(self, filename: str) -> typing.List[HelmRelease]:
        print(f'HelmStore import file :{filename}')
        classes = []
        if os.path.isfile(filename):
            with open(filename, 'r') as json_file:
                    helm_releases_list= json.load(json_file)
                    for helm_release in helm_releases_list:
                        items = HelmRelease(name='name', parent=None)
                        self._helm_to_classes(helm_release, items)
                        classes.append(items)

        else:
            print('File helm doesnt exists')
        return classes


    def _helm_to_classes(self, nested_dictionary: dict, parent: HelmRelease):
        for key, value in nested_dictionary.items():
            keys = f'{key}'
            if type(value) is dict:
                obj = HelmRelease(name=keys, parent=parent)
                parent.add_attribute(key, obj)
                self._helm_to_classes(value, obj)
            else:
                parent.add_attribute(keys, value)



    ############################### TESTOWANIE PROGRAMU##############################################################################################################
    '''test = NazwaKlasyStore("sciezka do pliku")
    print(test.nazwa_zmiennej_list.tutaj.twoje.klucze)'''
test = HelmStore('C:/Users/galanina/cilium-connection-matrix-generator/kind/output/helm_ls.json')

