from Engine.packet import Packet


def chunk(data: bytes, n: int) -> list[bytes]:
    return [data[i:i + n] for i in range(0, len(data), n)]


def make_packets(id_destination: int, data: bytes, size: int, max_seq_num_size: int) -> list[Packet]:
    data = chunk(data, size)
    packets_count = len(data)
    packets = []
    for i in range(packets_count):
        seq_num = i % max_seq_num_size
        packet = Packet(id_destination, seq_num, False, True, len(data[i]), data[i])
        packets.append(packet)
    return packets

