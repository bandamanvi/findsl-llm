import yaml

def load_dsl(path):
    with open(path, "r") as f:
        dsl = yaml.safe_load(f)
    return dsl
