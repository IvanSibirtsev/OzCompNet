from dataclasses import dataclass


@dataclass
class Config:
    max_packets_count: int
    max_data_size: int
    file_to_write: str
    file_to_read: str
    packets_in_section: int = 255
