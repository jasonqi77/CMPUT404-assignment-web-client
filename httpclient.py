#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
	if not port:
            port = 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        code = data.split()
	print "####"
	print code
	print "####"
	return int(code[1])


    def get_headers(self,data):
        headers = data.split('\r\n\r\n')
	return headers[0]

    def get_body(self, data):
        body = data.split('\r\n\r\n')
	return body[1]

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
        return str(buffer)

    def GET(self, url, args=None):
 	parseUrl = urlparse(url) 
	s = self.connect(parseUrl.hostname, parseUrl.port)
	msg = "GET %s HTTP/1.1\r\n" % (parseUrl.path)
	msg += "Host: %s\r\n" % (parseUrl.hostname)
	msg += "Accept: */*\r\n"
	msg += "Connection: close\r\n\r\n" 
	s.send(msg)
	response = self.recvall(s)
	s.close()
	code = self.get_code(response)
	body = self.get_body(response)      
        return HTTPRequest(code, body)

    def POST(self, url, args=None):       
        parseUrl = urlparse(url)
        s = self.connect(parseUrl.hostname, parseUrl.port)
	if (args == None):
		content = ""
	else:
		content = urllib.urlencode(args)
		
	content_length = len(content) 
	msg = "POST %s HTTP/1.1\r\n" % (parseUrl.path)
	msg += "Host: %s\r\n" % (parseUrl.hostname)
	msg += "Accept: */*\r\n"
	msg += "Content-Type: application/x-www-form-urlencoded\r\n"
	msg += "Content-Length: %s\r\n\r\n" % (str(content_length))
	msg += "%s\r\n" % (content)
	s.send(msg)
	response = self.recvall(s)
	print "!!!"
	print msg
	print "!!!"
	s.close()
	code = self.get_code(response)
	body = self.get_body(response)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
