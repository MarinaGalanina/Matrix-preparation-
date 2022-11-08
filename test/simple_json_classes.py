import json
FILENAME = 'hubble_observe_jsonpb.lst'



def read_json(filename):
    all_jsons = []
    with open(filename, 'r') as json_file:
        for line in json_file:
            all_jsons.append(json.loads(line))
    return all_jsons


def json_to_classes(nested_dictionary, parent):
    for key, value in nested_dictionary.items():
        keys = f'{key}'
        if type(value) is dict:
            obj = type(f'{key}', (parent,), dict())
            json_to_classes(value, obj)
            setattr(parent, f'{key}', obj)
        else:
            x = dict(value=f'{value}')
            object = type(keys, (parent,), x)
            setattr(parent, keys, object)


def pod_destinations(all_js):
    destination_pod = []
    for pod_name in all_js:
        if hasattr(pod_name.flow.destination,"pod_name"):
            destination_pod.append(pod_name.flow.destination.pod_name.value)
    return destination_pod


def main():
    all_data = read_json(FILENAME)

    all_js = []
    for data in all_data:
        js = type("Wrapper", (object,), dict())
        json_to_classes(data, js)
        all_js.append(js)


if __name__ == '__main__':
    main()


