from Engine.States.state import State
from Engine.packet import Packet
from Engine.data import make_packets


class SendData(State):
    def __init__(self, client, id_d: int):
        super().__init__(client)
        self._id_d = id_d
        data = self.read()
        self._packets = make_packets(id_d, data, client.config.max_data_size, client.config.packets_in_section)
        self._packet_seq_num = 0
        self._section = 1

    def read(self) -> bytes:
        with open(self._client.config.file_to_read, "rb") as file:
            return file.read()

    def send(self):
        i = 0
        print(self._section)
        while i < self._client.config.max_packets_count:
            if self._is_end_of_data(i):
                print("END OF DATA")
                self._client.send_end_of_data(self._id_d)
                return
            if self._id_end_of_section(i):
                print(f"UPDATE SECTION NUMBER TO {self._section}")
                self._section += 1
                self._packet_seq_num = 0
            offset = (self._section - 1) * self._client.config.packets_in_section
            packet_number = self._packet_seq_num + i + offset
            self._client.send_packet(self._packets[packet_number])
            i += 1
        self._packet_seq_num += i

    def _is_end_of_data(self, i: int) -> bool:
        offset = (self._section - 1) * self._client.config.packets_in_section
        return self._packet_seq_num + i + offset >= len(self._packets)

    def _id_end_of_section(self, i: int) -> bool:
        return self._packet_seq_num + i == self._client.config.packets_in_section

    def handle(self, packet: Packet):
        if packet.id != self._id_d:
            return
        self._packet_seq_num = packet.seq_num
        self.send()
