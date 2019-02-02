#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

PORT = 443
END_OF_LINE_RESPONSE = "\r\n"
PROTOCOL_RESPONSE = "HTTP/1.1"

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            return None
    # get status code
    def get_code(self, data):
        return None
    # get http headers
    def get_headers(self,data):
        return None
    # get http response body
    def get_body(self, data):
        return None

    def sendall(self, data):
        # self.socket.sendall(self.req_method.encode('utf-8'))
        # self.socket.sendall(self.req_requested_path.encode('utf-8'))
        # self.socket.sendall(self.req_protocol.encode('utf-8') + END_OF_LINE_RESPONSE.encode('utf-8'))
        # self.socket.sendall(self.req_url.encode('utf-8') + END_OF_LINE_RESPONSE.encode('utf-8'))
        # self.socket.sendall(self.req_accept.encode('utf-8') + END_OF_LINE_RESPONSE.encode('utf-8'))
        # self.socket.sendall(END_OF_LINE_RESPONSE.encode('utf-8'))


        # self.socket.sendall(data.encode('utf-8'))
        return None
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            print(part)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        # data = self.generate_request("GET", url)
        # self.sendall(data)
        # print("sent GET")

        # self.recvall(self.soc   ket)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        data = self.generate_request(sys.argv[2], sys.argv[1])
        self.sendall(data)
        print("sent POST")

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def generate_request(self, method, url):
        self.req_method = method + " "
        self.req_requested_path = "/ "
        self.req_protocol = PROTOCOL_RESPONSE
        self.req_url = r"Host: " + url
        self.req_accept = r"Accept: */*"

        return self.req_method +\
               self.req_requested_path +\
               self.req_protocol + END_OF_LINE_RESPONSE +\
               self.req_url + END_OF_LINE_RESPONSE +\
               self.req_accept + END_OF_LINE_RESPONSE + END_OF_LINE_RESPONSE
               # END_OF_LINE_RESPONSE +\
               # END_OF_LINE_RESPONSE +\
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        tmp = sys.argv[2].split(":")
        client.connect(tmp[0], int(tmp[1]))
        print(client.command(sys.argv[2], sys.argv[1]).body)
        # generate request here yooooo!
        # print(client.command( sys.argv[2], sys.argv[1] ).code)
    else:
        client.connect(sys.argv[1], PORT)

        print(client.command( sys.argv[1] ))

"""
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
'__format__', '__ge__', '__getattribute__', '__gt__', '__hash__',
'__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
'__str__', '__subclasshook__', '__weakref__', 'body', 'code']
"""
