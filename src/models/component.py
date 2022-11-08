import json
import yaml


class Component:

    def __init__(self, name=None, namespace=None, description=None):
        self.connections = []
        self.services = []
        self.ports = []
        self.transportLayer: str = ""
        self.name: str = name
        self.namespace: str = namespace
        self.description: str = description
        self.release: str = name

    def __repr__(self):
        return f'Component(name="{self.name}",namespace="{self.namespace}")'

    def update_connections(self, source) -> None:
        data = {
            "type": "internal",
            "destination": [{"service": "",
                             "portId": f"{self.DestinationPort}:{self.transportLayer}"}]
        }

        if data not in self.connections:
            self.connections.append(data)
            self.services[-1]['connections'].append(data)

    def update_ports(self, destination) -> None:
        data = {
            "id": f"{destination['identity']}:{self.transportLayer}",
            "port": f"{destination['identity']}",
            "transportLayer": f"{self.transportLayer}",
            "applicationLayer": "",
            "auth": "",
            "note": ""
        }
        if data not in self.ports:
            self.ports.append(data)
            self.services[-1]['ports'].append(data)

    def update_services(self, kubernetes_object) -> None:

        data = {"name": f"{kubernetes_object.name}",
                "displayName": f"{kubernetes_object.name}",
                "description": "",
                "ports": [],
                "connections": []}

        for service in self.services:
            if service["name"] == data['name'] and \
               service['displayName'] == data['displayName'] and \
               service['description'] == data['description']:
                return

        self.services.append(data)

    def update_transfer_leyer(self, conection):
        if hasattr(conection, 'TCP'):
            self.transportLayer = 'TCP'
        elif hasattr(conection, 'ICMPv4'):
            self.transportLayer = 'ICMPv4'
        elif hasattr(conection, 'UDP'):
            self.transportLayer = 'UDP'

    def update_portID(self, port_connection):
        if hasattr(port_connection,'UDP'):
           self.DestinationPort = port_connection.UDP.source_port
        if hasattr(port_connection,'TCP'):
            self.DestinationPort = port_connection.TCP.source_port
        if hasattr(port_connection,'ICMPv4'):
            self.DestinationPort = port_connection.ICMPv4.source_port


    def dump_to_file(self, output_dir) -> None:
        #if self.services:
            #print(f"{len(self.connections)=}")
            #self.services[0]["ports"] = self.ports
            #self.services[0]["connections"] = self.connections
        data = {
            "name": f"{self.name}",
            "displayName": f"{self.name}",
            "description": f"{self.description}",
            "services": self.services

        }
        with open(output_dir, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

#namespace do name
#zapisać każdy component w katalogu pod inną nazwą
#nazwa to nazwa componentu
#namiar do innego component
#przerobić