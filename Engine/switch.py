from Engine.connection import Connection
from Engine.localNetInformation import LocalNetInformation
from struct import unpack, pack


class Switch:
    def __init__(self, local_net_information: LocalNetInformation):
        self._local_net_information = local_net_information

    def run(self):
        connections = self._local_net_information.get_connections()
        ids = self._local_net_information.get_ids()
        while True:
            for conn in connections:
                data = conn.read(1)
                if not data:
                    continue
                id_d = unpack("< B", data)[0]
                if id_d not in ids:
                    continue
                id_s = conn.id
                packet = pack("< B", id_s) + self.read(conn)
                print(f"GET PACKET FROM {id_s} TO {id_d} PACKET: {packet}")
                self._local_net_information.get_connection_by_id(id_d)\
                    .write(packet)

    def read(self, conn: Connection) -> bytes:
        seq_num = conn.read(1)
        third = conn.read(1)
        size = unpack("< B", third)[0] & 63
        data = conn.read(size)
        return seq_num + third + data
