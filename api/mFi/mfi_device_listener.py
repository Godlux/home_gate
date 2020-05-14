import logging
import socket
import threading

log = logging.getLogger('udp_server')


class MfiListener( threading.Thread ):
    devices = dict()

    # udpserver
    def udp_server(self, host='192.168.1.52', port=10001):  # fixme: set host at config
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        log.info("Listening on udp %s:%s" % (host, port))
        s.bind((host, port))
        while True:
            (data, addr) = s.recvfrom(128*1024)
            yield data, addr

    def run(self):
        FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
        logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

        for data, addr in self.udp_server():
            log.debug(f"[{addr}] {data} | {data.decode('utf-8', 'backslashreplace')}")
            if addr in self.devices:
                continue
            self.devices[addr[0]] = data.decode('utf-8', 'backslashreplace')


if __name__ == "__main__":
    listener = MfiListener()
    listener.start()
