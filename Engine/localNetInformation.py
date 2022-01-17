from Engine.connection import Connection


class LocalNetInformation:
    def __init__(self):
        self._id_to_connection: dict[int, Connection] = {}
        self._connection_to_id: dict[Connection, int] = {}

    def add(self, id: int, connection: Connection):
        self._id_to_connection[id] = connection
        self._connection_to_id[connection] = id

    def get_ids(self) -> set[int]:
        return set(self._id_to_connection.keys())

    def get_connections(self) -> list[Connection]:
        return list(self._connection_to_id.keys())

    def get_connection_by_id(self, id: int) -> Connection:
        return self._id_to_connection[id]
