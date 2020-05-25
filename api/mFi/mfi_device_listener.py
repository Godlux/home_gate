import logging
import os, sys
import socket
import threading
from getmac import get_mac_address

log = logging.getLogger('udp_server')


class MfiListener( threading.Thread ):
	devices = dict()
	need_stop = False

	def prepare_to_listen( self, host='255.255.255.255', port=10001 ):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		s.settimeout( 2 )

		# send ( b'\x01\x00\x00\x00' ) signal to discover devices
		for i in range(10):
			s.sendto(b'\x01\x00\x00\x00', ('255.255.255.255', port))

		s.close()

	# udpserver
	def udp_server(self, host='localhost', port=10001):  # fixme: set host at config
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		log.info("Listening on udp %s:%s" % (host, port))
		s.bind((host, port))
		while True:
			(data, addr) = s.recvfrom(128*1024)
			yield data, addr

	def run(self):
		FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
		logging.basicConfig(level=logging.INFO, format=FORMAT_CONS)

		self.prepare_to_listen()
		host = ""  # listen all
		for data, addr in self.udp_server(host=host):
			mac = Util.get_mac(addr[0])
			log.debug(f"[ {addr} / {mac} ] {data} | {data.decode('utf-8', 'backslashreplace')}")
			log.info(f"[ {addr[0]} / {mac} ]")
			if addr in self.devices:
				continue
			if mac is None:
				continue

			ip = addr[0]
			port = addr[1]
			self.devices[str(mac)] = ip, port, mac, data

			if self.need_stop:
				break

	def stop( self ):
		self.need_stop = True


class Util( object ):
	@staticmethod
	def get_mac( ip ):
		ip_mac = get_mac_address(ip=ip)
		return ip_mac


if __name__ == "__main__":
	listener = MfiListener()
	listener.start()
