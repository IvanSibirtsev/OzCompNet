from Engine.States.state import State
from Engine.packet import Packet


class ReceiveData(State):
    def __init__(self, client, id_d: int):
        super().__init__(client)
        self._id_d = id_d
        self._count_of_received_packets = 0
        self._packets_in_section_count = client.config.packets_in_section
        self._max_packets_count = client.config.max_packets_count
        self._file_to_write = client.config.file_to_write

    def handle(self, packet: Packet):
        self._count_of_received_packets += 1
        if self._id_d == packet.id:
            self._handle_packet_from_session(packet)
        if self._is_buffer_full():
            requested_packet_number = self._get_packet_number()
            self._client.send_accept_packet(packet.id, requested_packet_number)

    def _get_packet_number(self) -> int:
        return self._count_of_received_packets % self._packets_in_section_count

    def _handle_packet_from_session(self, packet: Packet):
        if packet.is_end_of_data():
            self._client.handle_end_of_data()
            return
        print(packet.data)

        with open(self._file_to_write, "ab") as file:
            file.write(packet.data)

    def _is_buffer_full(self) -> bool:
        return self._count_of_received_packets % self._max_packets_count == 0
