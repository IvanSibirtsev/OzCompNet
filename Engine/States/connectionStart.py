from Engine.States.state import State
from Engine.packet import Packet


class ConnectionStart(State):
    def __init__(self, client):
        super().__init__(client)

    def send(self):
        self._client.send_request()

    def handle(self, packet: Packet):
        self._client.end_connection(packet)
