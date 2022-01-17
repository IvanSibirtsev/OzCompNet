class Config:
    def __init__(self, max_data_size: int, max_packets_count: int, file_to_write: str, file_to_read: str):
        self.max_packets_count = max_packets_count
        self.max_data_size = max_data_size
        self.file_to_write = file_to_write
        self.file_to_read = file_to_read
        self.packets_in_section = 255
