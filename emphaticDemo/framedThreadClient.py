#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import params
from framedSock import FramedStreamSock
from threading import Thread
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
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

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("          creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print("      error: %s" % msg)
               s = None
               continue
           try:
               print("              attempting to connect to %s" % repr(sa))
              # print("im the sa witout repr " + str( serverHost))
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
           
       while(True): 
            fs = FramedStreamSock(s, debug=debug)
            userInput = input("Enter the file name you wish to send or type ""exit"" to exit the program \n")
            
            if (userInput != "exit"):
                try:
                    with open(userInput,"r") as file:
                        fileline  = file.read().split("\n")
						#print(fileline)
						
                        i=0
                    for stringLine in fileline:
                        if(stringLine != '' or stringLine != ' '):
                            fs.sendmsg(fileline[i].encode())
                            print("received:", fs.receivemsg())
                            i+=1
                    file.close()
                except IOError:
                    print("File does not exist in this directory")
            else:
                break

ClientThread(serverHost, serverPort, debug)