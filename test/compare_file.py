import simple_json_classes as simp_js
import simple_yaml_classes as simp_yam

def compare_function(list_a, list_b):
    common_elements = list(set(list_a) & set(list_b))

