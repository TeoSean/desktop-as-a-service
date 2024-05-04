import json
import yaml

config = json.loads(open("config/config.json", "r").read())

with open("config/base/base.yml", "r") as file:
    base = file.read()

with open("config/base/lb.yml", "r") as file:
    lb_base = yaml.safe_load(file)

for _global in config["globals"]:
    base = base.replace("${{globals."+_global+"}}", config["globals"][_global])

box_bases = []
box_configs = []
for box in config["boxes"]:
    box_base = base
    box_configs.append(box)
    for _conf in box:
        box_base = box_base.replace("${{config."+_conf+"}}", str(box[_conf]))
    
    box_bases.append(yaml.safe_load(box_base))

ports = []
for base, config in zip(box_bases, box_configs):
    ports.append(
            {
                "name": config["name"] + "-lb",
                "port": config["port"],
                "targetPort": config["name"] + "-port"
                }
            )

lb_base['spec']['ports'] = ports

box_bases.append(lb_base)
with open("build/out.yaml", "w+") as file:
    yaml.dump_all(box_bases, file, default_flow_style=False)
