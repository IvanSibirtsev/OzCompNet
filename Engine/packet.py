import struct


class Packet:
    _EOL = b"EOL"

    def __init__(self, id: int, seq_num: int, syn: bool, seq: bool, size: int, data: bytes):
        self.id = id
        self.seq_num = seq_num
        self.syn = syn
        self.seq = seq
        self.size = size
        self.data = data

    def __bytes__(self) -> bytes:
        packet = struct.pack("< B", self.id)
        packet += struct.pack("< B", self.seq_num)
        flags = Packet._make_flags(self.syn, self.seq)
        packet += struct.pack("< B", (flags << 6) + self.size)
        packet += self.data
        return packet

    @staticmethod
    def _make_flags(syn: bool, seq: bool) -> int:
        if syn and seq:
            return 0b11
        if syn:
            return 0b10
        if seq:
            return 0b01
        return 0b00

    def is_end_of_data(self) -> bool:
        return not self.seq and self.syn and self.data == Packet._EOL

    @staticmethod
    def request(id: int) -> "Packet":
        return Packet(id, 0, True, False, 0, b"")

    @staticmethod
    def accept_session(id: int) -> "Packet":
        return Packet(id, id + 1, True, False, 0, b"")

    @staticmethod
    def accept(id: int, seq_num: int) -> "Packet":
        return Packet(id, seq_num, True, True, 0, b"")

    @staticmethod
    def end_of_data(id: int) -> "Packet":
        eol = Packet._EOL
        return Packet(id, 0, True, False, len(eol), eol)

    def to_str(self):
        return f"id: {self.id}, seq num: {self.seq_num}, syn: {self.syn}, seq: {self.seq}, data: {self.data}"
