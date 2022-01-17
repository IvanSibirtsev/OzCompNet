from Engine.packet import Packet


class State:
    def __init__(self, client):
        self._client = client

    def handle(self, packet: Packet):
        pass
