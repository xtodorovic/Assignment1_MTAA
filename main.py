import sys

import sipfullproxy
import logging
import time

record_route = ""
via = ""
PORT = ''
HOST = 0
ip_address = ""


def getVariablesFromLibrary():
    return sipfullproxy.recordroute, sipfullproxy.topvia, sipfullproxy.PORT, sipfullproxy.HOST, sipfullproxy.socket.gethostname()


def getHostnameAndIpAddressFromSocket():
    global HOST
    return sipfullproxy.socket.gethostname(), sipfullproxy.socket.gethostbyname(HOST)


def LogCommunicationData():
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', filename='proxy.log', level=logging.INFO,
                        datefmt='%H:%M:%S')
    logging.info(time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()))
    global ip_address
    host_name, ip_address = getHostnameAndIpAddressFromSocket()

    logging.info(host_name)

    if ip_address == "127.0.0.1":
        ip_address = sys.argv[1]

    logging.info(ip_address)


def StartServer(recordroute, to_proxy_via, ip_address, port, host):
    recordroute = "Record-Route: <sip:%s:%d;lr>" % (ip_address, port)
    sipfullproxy.recordroute = recordroute

    to_proxy_via = "Via: SIP/2.0/UDP %s:%d" % (ip_address, PORT)
    sipfullproxy.topvia = to_proxy_via

    server = sipfullproxy.socketserver.UDPServer((host, port), sipfullproxy.UDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    record_route, via, PORT, HOST, hostname = getVariablesFromLibrary()
    LogCommunicationData()
    StartServer(record_route, via, ip_address, PORT, HOST)
