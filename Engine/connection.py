import serial
from struct import unpack, pack


class Connection:
    def __init__(self, name: str, id: int, timeout: float):
        self._timeout = timeout
        self._name = name
        self.id = id
        self._connection = self._open_connections()

    def _open_connections(self) -> serial.Serial:
        return serial.Serial(self._name, timeout=self._timeout)

    def read(self, n: int) -> bytes:
        return self._connection.read(n)

    def read_packet(self) -> bytes:
        data = self._connection.read(3)
        if not data:
            return b""
        id_d, seq_num, third = unpack("< B B B", data)
        data = self._connection.read(third & 63)
        return pack("< B B B", id_d, seq_num, third) + data

    def write(self, data: bytes):
        self._connection.write(data)
