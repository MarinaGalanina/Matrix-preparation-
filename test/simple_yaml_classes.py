import yaml
import simple_json_classes as simp
FILENAME = 'new_test.yaml'

all_yaml = []
    with open(filename,'r') as yaml_file:
        configuration = yaml.safe_load(yaml_file)
    return configuration['items']
def read_yaml(filename):



def yaml_to_classes(nested_dictionary, parent):
    for key, value in nested_dictionary.items():
        keys=f'{key}'
        if type(value) is dict:
            obj = type(keys, (parent,), dict())
            yaml_to_classes(value, obj)
            setattr(parent, keys, obj)
        else:
            # setattr(parent, f'{key}', f'{value}')
            x = dict(value=f'{value}')
            object = type(keys, (parent,),x)
            setattr(parent, keys, object)


def pod_finding(all_js):
    list_of_pods = []
    for pod in all_js:
        if pod.kind.value == "Pod":
            if hasattr(pod.metadata, "name"):
                list_of_pods.append(pod.metadata.name.value)
    return list_of_pods

def node_finding(all_js):
    list_of_nodes=[]

def main():
    all_data = read_yaml(FILENAME)

    all_yaml = []
    for data in all_data:
        yaml = type("Wrapper", (object,), dict())
        yaml_to_classes(data, yaml)
        all_yaml.append(yaml)


if __name__ == '__main__':
    main()
