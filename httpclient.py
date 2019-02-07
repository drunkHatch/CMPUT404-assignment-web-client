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
import json
# you may use urllib to encode data appropriately
import urllib.parse as parser

END = "\r\n"
ERROR = "Error code:"
HTTP_DEFAULT_PORT = 80

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

    def get_code(self, data):
        lines = data.split("\n")

        for line in lines:
            if ERROR in line:
                tmp = line
                tmp = tmp.replace("<p>", "")
                tmp = tmp.replace("</p>", "")
                tmp = tmp.replace(ERROR, "")
                tmp = tmp.replace(" ", "")

                return int(tmp)

        lines = data.split("\n")
        if "HTTP/1.1" in lines[0]:
            tmp = lines[0]
            tmp = tmp.replace("HTTP/1.1 ", "")

            try:
                return int(tmp[0:3])
            except Exception as e:
                print("fail to catch status code")
                return 500

        return 200

    def get_headers(self,data):
        head_body = data.split("\r\n\r\n")
        return head_body[0]

    def get_body(self, data):
        head_body = data.split("\r\n\r\n")
        if len(head_body) == 1: # nobody
            return ""
        else: # body exists
            return head_body[1]

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        parse_result = parser.urlparse(url)
        addr = parse_result.netloc.split(":")
        if len(addr) == 1:
            self.connect(addr[0], HTTP_DEFAULT_PORT)
        else:
            self.connect(addr[0], int(addr[1]))
        data = self.generate_request("GET", parse_result)
        self.sendall(data)
        response = self.recvall(self.socket)
        code = self.get_code(response)
        body = self.get_body(response)
        if len(body) == 0:
            body = ""
            pass
        else:
            print(body)

        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        json_args = None
        code = 500
        body = ""
        if args:
            # sending_body = self.generate_body(args)
            sending_body = parser.urlencode(args)
        else:
            sending_body = parser.urlencode("")
        parse_result = parser.urlparse(url)
        addr = parse_result.netloc.split(":")
        if len(addr) == 1:
            self.connect(addr[0], HTTP_DEFAULT_PORT)
        else:
            self.connect(addr[0], int(addr[1]))
        data = self.generate_request("POST", parse_result, len(sending_body))
        data += sending_body
        self.sendall(data)
        response = self.recvall(self.socket)
        code = self.get_code(response)
        body = self.get_body(response)
        if len(body) == 0:
            body = ""
            pass
        else:
            print(body)
        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def generate_request(self, method, parse_result, length=-1):
        if method == "POST":
            req_method = method + " "
            if len(parse_result.path) == 0:
                req_path = "/ "
            else:
                req_path = parse_result.path + " "
            req_protocol = "HTTP/1.1" + END
            req_host = "Host: " + parse_result.netloc + END
            req_cont_type = "Content-Type: application/x-www-form-urlencoded" + END
            if length != -1:
                req_cont_length = "Content-Length: " + str(length) + END
                return req_method + req_path + req_protocol + req_host + req_cont_type + req_cont_length + "Connection: close" + END + END

            return req_method + req_path + req_protocol + req_host + req_cont_type + "Connection: close" + END + END

        req_method = method + " "
        if len(parse_result.path) == 0:
            req_path = "/ "
        else:
            req_path = parse_result.path + " "
        req_protocol = "HTTP/1.1" + END
        req_host = "Host: " + parse_result.netloc + END

        return req_method + req_path + req_protocol + req_host + "Connection: close" + END + END

    def generate_body(self, content, type="def"):
        if type == "def":
            buffer = bytearray()
            content_list = []
            result_body = r""
            length = 0
            for each in content:
                buffer.extend((each + "=" + content[each] + "&").encode("utf-8"))
            return buffer[:-1].decode("utf-8")
        elif type == "json":
            return None

        # length = len(content)
        # for i in range(length):
        #     if i != (length - 1):
        #         result_body += content_list[i] + "&"
        #     else:
        #         result_body += content_list[i]


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        client.command( sys.argv[2], sys.argv[1] )
    else:
        client.command( sys.argv[1] )
