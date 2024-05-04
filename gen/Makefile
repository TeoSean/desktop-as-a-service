default: build-config build-rest

build-rest:
	python3 generate_kubeconf.py
	python3 generate_html.py

build-config:
	cd config && python3 generate_config.py

discord:
	python3 discord_bot.py

all: build-config build discord
