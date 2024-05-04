import json

config = json.loads(open("config/config.json").read())

html_doc="<!DOCTYPE html><html><body style=\"display: grid; grid-template-columns: repeat(3, 600px);\">"

for box in config["boxes"]:
    port = box["port"]
    name = box["name"]
    passwd = box["novnc_password"]
    html_doc += f"<div><p>{name}</p><iframe width=\"600\" height=\"400\" src=\"http://boxes.dunhack.me:{port}/vnc.html?password={passwd}&path=vnc&autoconnect=true&resize=scale&reconnect=true&show_dot=true\"></iframe></div>"

html_doc += "</body></html>"
with open("build/out.html", "w+") as file:
    file.write(html_doc)
