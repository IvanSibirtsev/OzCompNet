from Engine.connection import Connection
from Engine.States.connectionAccept import ConnectionAccept
from Engine.States.connectionStart import ConnectionStart
from Engine.States.ReceiveData import ReceiveData
from Engine.States.SendData import SendData
from Engine.parser import Parser
from Engine.packet import Packet
from Engine.config import Config


class Client:
    def __init__(self, id: int, flag: bool, connection: Connection, config: Config, id_d: int = -1):
        self.config = config
        self._id = id
        self._flag = flag
        self._connection = connection
        self._state = ConnectionAccept(self)
        self._id_d = id_d

    def run(self):
        if self._flag:
            self._state = ConnectionStart(self)
            self._state.send()
        while True:
            self._read_channel()

    def _read_channel(self):
        data = self._connection.read_packet()
        if data:
            print(f"{self._id}: RECEIVE {data}")
            self._handle_connection(data)

    def _handle_connection(self, data: bytes):
        parser = Parser()
        packet = parser.parse(data)
        print(packet.to_str())
        self._state.handle(packet)

    def send_request(self):
        packet = Packet.request(self._id_d)
        print(f"{self._id} SEND REQUEST:", packet.to_str())
        self._connection.write(bytes(packet))

    def send_session_accept(self, packet: Packet):
        accept = Packet.accept_session(packet.id)
        print(f"{self._id} SEND ACCEPT:", accept.to_str())
        self._connection.write(bytes(accept))
        self._state = ReceiveData(self, packet.id)

    def end_connection(self, packet: Packet):
        if packet.seq_num == self._id + 1:
            print("SUCCESS CONNECTION")
            self._state = SendData(self, self._id_d)
            self._state.send()

    def send_packet(self, packet):
        print(f"{self._id} SEND PACKET {packet.to_str()}")
        self._connection.write(bytes(packet))

    def send_accept_packet(self, id: int, seq_num: int):
        packet = Packet.accept(id, seq_num)
        print(f"SEND ACCEPT PACKET {packet.to_str()}")
        self._connection.write(bytes(packet))

    def send_end_of_data(self, id: int):
        packet = Packet.end_of_data(id)
        self._state = ConnectionAccept(self)
        self._connection.write(bytes(packet))

    def handle_end_of_data(self):
        self._state = ConnectionAccept(self)
