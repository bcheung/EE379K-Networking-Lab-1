#!/usr/bin/env python3
from socket import *

def main():
    target_host = "www.baiwanzhan.com"
    target_port = 80  # create a socket object
    query_params = "/service/site/search.aspx?query=hi"
    client = socket(AF_INET, SOCK_STREAM)

    # connect the client
    client.connect((target_host,target_port))

    # send some data
    request = "GET {} HTTP/1.1\r\nHost:{}\r\n\r\n".format(query_params, target_host)
    client.send(request.encode())

    # receive some data
    response = client.recv(4096)
    http_response = repr(response)
    http_response_len = len(http_response)

    #display the response
    print("[RECV] - length: %d" % http_response_len)
    print(http_response)

if __name__ == "__main__":
    # try:
    #     os.mkdir("results")
    #     main()
    # except Exception:
    #     print("Must delete results directory to run script")
    main()
