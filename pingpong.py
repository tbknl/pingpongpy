#!/usr/bin/env python

import argparse
import socket
import sys
import string
import random
import time
import numpy


def pong_server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		sock.bind((host, port))
	except socket.error as err:
		print("Socket bind failed.", err)
		sys.exit(1)

	sock.listen(0)
	print("Listening on {0}:{1}...".format(host, port))
	try:
		while True:
			conn, addr = sock.accept()
			print("Incoming connection from {0}:{1}".format(*addr))
			file_wrapper = conn.makefile("r")
			try:
				while True:
					line = file_wrapper.readline()
					if not line:
						break
					cmd = line.split()
					if len(cmd) >= 2 and cmd[0] == "ping":
						pong_size = 0
						try:
							pong_size = max(0, int(cmd[1]))
						except ValueError:
							pass
						conn.send("pong ")
						while pong_size > 0:
							chunk_size = min(pong_size, 4096)
							data = 'Y' * chunk_size
							conn.send(data)
							pong_size -= chunk_size
						conn.send("\n")
					else:
						print("Invalid command received.")
						break
			except socket.error:
				pass
			finally:
				file_wrapper.close()
				conn.close()
				print("Connection closed.")
	except KeyboardInterrupt:
		print("Interrupted. Shutting down.")

	sock.close()


def ping(host, port, ping_size = 10, pong_size = 500000, seconds = 10):
	roundtrips = []
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((host, port))
		file_wrapper = sock.makefile("r")
		start_time = time.time()
		try:
			r = 1
			now = 0
			print("seq\troundtrip-time\telapsed-time")
			while now < start_time + seconds:
				t0 = time.time()
				sock.send("ping {0} ".format(pong_size))
				data_left = ping_size
				while data_left > 0:
					chunk_size = min(data_left, 4096)
					data = 'X' * chunk_size
					sock.send(data)
					data_left -= chunk_size
				sock.send("\n")
				line = file_wrapper.readline()
				now = time.time()
				dt = now - t0
				roundtrips.append(dt)
				print("{0}\t{1}\t{2}".format(r, dt, now - start_time))
				r += 1
		finally:
			file_wrapper.close()
	except KeyboardInterrupt:
		print("Interrupted. Shutting down.")
	except:
		print("Unexpected exception: {0}".format(sys.exc_info()))
	finally:
		sock.close()
		print("Connection closed.")

	print("Roundtrips: {count}".format(count=len(roundtrips)))
	print("Average: {average}".format(average=numpy.mean(roundtrips)))
	print("Min: {min}".format(min=numpy.min(roundtrips)))
	print("Max: {max}".format(max=numpy.max(roundtrips)))
	print("Stddev: {stddev}".format(stddev=numpy.std(roundtrips)))


if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("mode", type=str, choices=['ping', 'pong'], help="program mode")
	argparser.add_argument("host", type=str, help="host ip address (in pong mode 'ALL' indicates bind to all addresses)")
	argparser.add_argument("port", type=int, help="tcp port")
	argparser.add_argument("--ping-size", type=int, default=10000, help="ping payload size (only in ping mode)")
	argparser.add_argument("--pong-size", type=int, default=500, help="pong payload size (only in ping mode)")
	argparser.add_argument("--seconds", type=int, default=30, help="duration in seconds (only in ping mode)")
	args = argparser.parse_args()

	if args.mode == 'pong':
		host = '0.0.0.0' if args.host == 'ALL' else args.host
		pong_server(host, args.port)
	else:
		try:
			host = socket.gethostbyname(args.host)
		except:
			print("Could not resolve host '{0}'.".format(args.host))
			exit(1)

		ping(host, args.port, ping_size=args.ping_size, pong_size=args.pong_size, seconds=args.seconds)

