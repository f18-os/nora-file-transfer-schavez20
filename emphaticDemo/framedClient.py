#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import os
import params
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
while (True):
	fs = FramedStreamSock(s, debug=debug)

	#lets work on the user iput 
	stringIn = input("enter the name of the file enter exit to finish\n")
	#print(stringIn)
	if(stringIn != "exit"):
		infile = open(stringIn,"r")
		for line in infile:
			print(line.encode())
			fs.sendmsg(line.encode())
		print("received:", fs.receivemsg())
	else:
	 	break
#fs.sendmsg(b"hello world")
#print("received:", fs.receivemsg())

#fs.sendmsg(b"hello world")
#print("received:", fs.receivemsg())

