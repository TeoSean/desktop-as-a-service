import json
import random
import string

with open("config.json", "r") as file:
    config = json.loads(file.read())

with open("people", "r") as file:
    people = file.read().split('\n')
    people.remove("")

config["boxes"] = []
ports = random.sample(range(*map(int, config["port_range"].split("-"))), len(people))


for person, port in zip(people, ports):
    name, uid = person.split(" ")
    config["boxes"].append(
                {
                "name": name,
                "port": port,
                "discord_uid": uid,
                "novnc_password": ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                }
            )
with open("config.json", "w") as file:
    file.write(json.dumps(config, indent=4))

