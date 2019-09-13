#!/usr/bin/env python3
from socket import *

def main():
    target_host = "www.baiwanzhan.com"
    target_port = 80  # create a socket object
    client = socket(AF_INET, SOCK_STREAM)

    # connect the client
    client.connect((target_host,target_port))

    # send some data
    # normal GET request
    query_params = "/service/site/search.aspx?query=hi"
    # request = "GET {} HTTP/1.1\r\nHost:{}\r\n\r\n".format(query_params, target_host)
    # client.send(request.encode())

    # split GET request into 2 packets
    packet_1 = "GET /service/site/search.aspx?query=%E6%B3%95"
    packet_2 = "%E8%BD%AE HTTP/1.1\r\nHost:{}\r\n\r\n".format(target_host)
    client.send(packet_1.encode())
    client.send(packet_2.encode())

    # receive some data
    response = client.recv(4096)
    http_response = repr(response)
    http_response_len = len(http_response)

    #display the response
    print("[RECV] - length: %d" % http_response_len)
    print(http_response)

if __name__ == "__main__":
    main()
