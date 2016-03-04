#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from proxy import *
import zlib
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from lxml import html

class MyProxy(Proxy):

    def _process_response(self, data):
        # parse incoming response packet
        # only for non-https requests
        if not self.request.method == b"CONNECT":
            self.response.parse(data)

        if self.server:
            if self.server.addr[0] == 'habrahabr.ru':
                try:
                    tree = html.fromstring(data)
                    element = tree.xpath('//div[@class="content_left"]/div[@class="post_show"]/div[@class="post"]/div[@class="content"]') 
                    try:
                        text = element[0].text
                        words = text.split(' ')
                        for index in range(len(words)):
                            if len(words[index]) == 4:
                                words[index] = words[index]+'"-CHOCO"'

                        text = " ".join(words)
                        element[0].text = text
                        data = html.tostring(tree)
                    except:
                        pass
                except:
                    pass

        # queue data for client
        self.client.queue(data)

class MyHTTP(HTTP):
   
    def handle(self, client):
        proc = MyProxy(client)
        proc.daemon = True
        proc.start()
        logger.debug('Started process %r to handle connection %r' % (proc, client.conn))

def main():
    parser = argparse.ArgumentParser(
        description='asdf',
        epilog='asdfsad'
    )
    
    parser.add_argument('--hostname', default='127.0.0.1', help='Default: 127.0.0.1')
    parser.add_argument('--port', default='8899', help='Default: 8899')
    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO, WARNING, ERROR, CRITICAL')
    args = parser.parse_args()
    
    logging.basicConfig(level=getattr(logging, args.log_level), format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')
    
    hostname = args.hostname
    port = int(args.port)
    
    try:
        proxy = MyHTTP(hostname, port)
        proxy.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()