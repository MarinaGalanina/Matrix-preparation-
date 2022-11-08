import typing
import json
import os


# mapa dla destination


class ConnectionPeer:
    def __init__(self):
        self.podname = None
        self.namespacename = None


# source-typ klasy connectionpeer+destination
class ConnectionFlow:
    def __init__(self, parent, name, source, destination):
        self.destination = destination
        self.source = source
        self.myself: str = name
        self.parent: ConnectionFlow = parent

    def get_top_parent(self):
        return self.parent

    def add_attribute(self, name, val):
        setattr(self, f'{name}', val)

    def __repr__(self):
        return f'ConnectionFlow(destination="{self.destination}",source={self.source}")'


class HubbleStore:

    def __init__(self, filename: str):
        self.connections_list = self._load(filename)

    def _load(self, filename: str) -> typing.List[ConnectionFlow]:
        print(f'HubbleStore import file :{filename}')
        classes = []
        if os.path.isfile(filename):
            with open(filename, 'r') as json_file:
                for dane in json_file:
                    data = json.loads(dane)
                    items = ConnectionFlow(name='items',
                                           parent=None,
                                           source=data['flow']["source"],
                                           destination=data['flow']["destination"])

                    self._hubble_to_classes(data, items)
                    classes.append(items)

        else:
            print('File hubble doesnt exists')
        return classes

    def _hubble_to_classes(self, nested_dictionary: dict, parent: ConnectionFlow):
        for key, value in nested_dictionary.items():
            keys = f'{key}'
            if type(value) is dict:
                obj = ConnectionFlow(name=keys, parent=parent, source=None, destination=None)
                parent.add_attribute(key, obj)
                self._hubble_to_classes(value, obj)

            else:
                parent.add_attribute(keys, value)

    def _destination_get(self, destination: ConnectionFlow):
        for item in self.connections_list:
            if item.flow.destination is not None:
                destination.add

    ###############################TESTOWANIE PROGRAMU##############################################################################################################


test = HubbleStore('C:/Users/galanina/cilium-connection-matrix-generator/test/hubble_observe_jsonpb.lst')
