from argparse import ArgumentParser
from Engine.connection import Connection
from Engine.client import Client
from Engine.config import Config

HOME = "/home/iva/"


def main():
    parser = ArgumentParser(description="intercepts network traffic")
    parser.add_argument('-s', dest='session', type=int)
    parser.add_argument('-i', dest='id', type=int)
    parser.add_argument('-d', dest='destination', type=int)
    arg = parser.parse_args()
    path = f"{HOME}hosts/{arg.id}/"
    conn1 = Connection(path + str(arg.id), arg.id, 0.5)
    config = Config(10, 4, path + "out.txt", path + "in.txt")
    if arg.session == 0:
        Client(arg.id, False, conn1, config).run()
    else:
        print("START SESSION")
        Client(arg.id, True, conn1, config, arg.destination).run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

