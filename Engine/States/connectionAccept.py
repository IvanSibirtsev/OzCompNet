from Engine.States.state import State
from Engine.packet import Packet


class ConnectionAccept(State):
    def __init__(self, client):
        super().__init__(client)

    def handle(self, packet: Packet):
        self._client.send_session_accept(packet)
