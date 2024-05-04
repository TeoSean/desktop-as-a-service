from python_on_whales import docker, Image, Container
from dataclasses import asdict
from typing import Dict
import threading
import psycopg2
import json
import time


class Challenge:
    challenge_id: str
    image: Image
    docker_opts: Dict[str, str|int]
    port: int

class Instance:
    instance_id: str
    container: Container
    challenge: Challenge
    exposed_port: int
    time_started: int

class ChallengeNotFound(Exception):
    pass

class InstanceNotFound(Exception):
    pass

class InstanceCapReached(Exception):
    pass


class Runner:
    def __init__(self, db, instance_cap=5):
        self.db = db
        self.instance_cap = instance_cap
        self.current_instances = 0
        self.lock = threading.Lock()
    def register_challenge(self, challenge: Challenge) -> None:
        cur = self.db.cursor()
        cur.execute("INSERT INTO challenges (id, image_id, docker_opts, port) VALUES (%s, %s, %s, %s)", (challenge.challenge_id, challenge.image.id, json.dumps(challenge.docker_opts), challenge.port))

    def register_instance(self, instance: Instance) -> None:
        cur = self.db.cursor()
        cur.execute("INSERT INTO instances (id, container_id, challenge_id, port, time_started) VALUES (%s, %s, %s, %s, %s)", (instance.instance_id, instance.container.id, instance.challenge.challenge_id, instance.exposed_port, instance.time_started))

    def retrieve_challenge(self, challenge_id: str) -> Challenge:
        cur = self.db.cursor()
        cur.execute("SELECT id, image_id, docker_opts, port FROM challenges WHERE id=%s", (challenge_id,))
        c = cur.fetchone()
        if not c:
            raise ChallengeNotFound(challenge_id)
        return Challenge(challenge_id=c[0], image=docker.image.inspect(c[1]), docker_opts=json.loads(c[2]), port=c[3])

    def retrieve_instance(self, instance_id: str) -> Instance:
        cur = self.db.cursor()
        cur.execute("SELECT id, container_id, challenge_id, port, time_started FROM instance WHERE id=%s", (instance_id,))
        c = cur.fetchone()
        if not c:
            raise InstanceNotFound(instance_id)
        return Challenge(challenge_id=c[0], container=docker.container.inspect(c[1]), challenge=self.retrieve_challenge(c[2]), exposed_port=c[3], time_started=c[4])

    def remove_challenge(self, challenge: Challenge) -> None:
        cur = self.db.cursor()
        cur.execute("DELETE FROM challenges WHERE id=%s", (challenge.challenge_id,))

    def remove_instance(self, instance: Instance) -> None:
        cur = self.db.cursor()
        cur.execute("DELETE FROM instances WHERE id=%s", (instance.instance_id,))

    def spawn(self, challenge: Challenge) -> Instance:
        if self.current_instances >= self.instance_cap:
            raise InstanceCapReached
        container = docker.container.create(challenge.image, **challenge.docker_opts, publish=[(0, challenge.port)])
        container.start()
        port = int(container.network_settings.ports[0]["HostPort"])
        instance = Instance(container=container, challenge=challenge, exposed_port=port, time_started=int(time.time()))
        self.register_instance(instance)
        self.current_instances += 1
        return instance

    def destroy(self, instance: Instance) -> None:
        self.lock.acquire()
        if instance.container.state.running:
            instance.container.stop()
        instance.container.remove()
        self.current_instances -= 1
        self.remove_instance(instance)
        self.lock.release()

    def purge(self) -> None:
        cur = self.db.cursor()
        cur.execute("SELECT id FROM instances")
        instance_ids = cur.fetchall()
        for instance_id in instance_ids:
            instance = self.retrieve_instance(instance_id[0])
            if int(time.time()) - instance.time_started > 1800:
                self.destroy(instance)
                continue
            if not instance.container.state.running:
                self.destroy(instance)

    def _purge_target(self):
        while True:
            self.purge()
            time.sleep(1)

    def start_purge_thread(self):
        self.thread = threading.Thread(target=self._purge_target)
        self.thread.start()


