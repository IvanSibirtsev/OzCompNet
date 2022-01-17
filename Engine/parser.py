import struct
from Engine.packet import Packet


class Parser:
    def parse(self, raw_data: bytes):
        id, seq_num, flags = struct.unpack("< B B B", raw_data[0:3])
        syn, seq = self._parse_flags(flags)
        size = flags & 63
        data = raw_data[3:]
        return Packet(id, seq_num, syn, seq, size, data)

    def _parse_flags(self, flags: int) -> tuple[bool, bool]:    # SYN, SEQ
        flags >>= 6
        match flags:
            case 0:
                return False, False
            case 1:
                return False, True
            case 2:
                return True, False
            case 3:
                return True, True
