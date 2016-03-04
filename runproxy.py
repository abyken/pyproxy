#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zlib
import logging
import argparse
from proxy import *
from lxml import html
from http_parser.http import HttpStream
from http_parser.reader import SocketReader

class MyProxy(Proxy):
    '''
    Inherited class of proxy.Proxy class, which is HTTP proxy implementation.
    Accepts connection object and act as a proxy between client and server.
    '''

    def _process_response(self, data):
        '''
            Method has been overrided because response body should be changed
        '''
        if not self.request.method == b"CONNECT":
            self.response.parse(data)

        #if self.server not None(initially, it is), method checks address
        #then finds "content" element of the page(using lxml library), find all words with
        #length 5  and add to the word "-CHOCO". Finally, set new data to client queue
        if self.server:
            if self.server.addr[0] == 'habrahabr.ru':
                try:
                    decompressed_data=zlib.decompress(data, 16+zlib.MAX_WBITS)
                    tree = html.fromstring(decompressed_data)
                    element = tree.xpath('//div[@class="content_left"]/\
                                          div[@class="post_show"]/\
                                          div[@class="post"]/div[@class="content"]') 
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

        # queue data for client
        self.client.queue(data)


class MyHTTP(HTTP):
    '''
    Inherited class of proxy.HTTP class, which is HTTP proxy implementation.
    Accepts connection object and act as a proxy between client and server.
    '''

    def handle(self, client):
        #has been overrided because of new Proxy class
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
    
    logging.basicConfig(level=getattr(logging, args.log_level), \
                                      format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')
    
    hostname = args.hostname
    port = int(args.port)
    
    try:
        proxy = MyHTTP(hostname, port)
        proxy.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()