from os import listdir

from Engine.localNetInformation import LocalNetInformation
from Engine.switch import Connection, Switch

HOME = "/home/iva/"


def main():
    ids = find_all_host_ids(HOME + "switch/")
    local_net_information = fill_local_net_information(ids)
    switch = Switch(local_net_information)
    switch.run()


def fill_local_net_information(ids: list[int]) -> LocalNetInformation:
    local_net_information = LocalNetInformation()
    for id in ids:
        local_net_information.add(id, Connection(HOME + f"switch/{id}", id, 0))
    return local_net_information


def find_all_host_ids(path: str) -> list[int]:
    return list(map(int, listdir(path)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
