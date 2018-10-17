import time
import zmq
import json
import os

_basepath = os.path.abspath(os.path.dirname(__file__))
conf = json.load(open(os.path.abspath(os.path.dirname(__file__))+"\\conf.json"))

class publisher:
    def __init__(self, bindserver,port,pub_key,pub_data=''):
        self.server = bindserver
        self.port = port
        #self.timestamp = timestamp
        self.key = pub_key
        self.data = pub_data

    def publish_newblock(self,**block):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://{}:{}".format(self.server,self.port))

        block_string = json.dumps(block['data'].__dict__, sort_keys=True)

        i = 0
        while True:
            publisher.send_multipart([b'new_block', bytes(block_string,'utf-8')])
            time.sleep(2)
            print(i)
            i+=1
            if i==2:
                break

        publisher.close()
        context.term()


    def publish_write_newblock(self,block):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://{}:{}".format(self.server,self.port))

        block_string = json.dumps(block, sort_keys=True)

        i = 0
        while True:
            publisher.send_multipart([b'write_block', bytes(block_string,'utf-8')])
            time.sleep(2)
            print(i)
            i+=1
            if i==2:
                break

        publisher.close()
        context.term()

    def req_rep(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://{}:{}".format(self.server,self.port))

        while True:
            #  Wait for next request from client
            data = socket.recv()
            data_str = data.decode(encoding="utf-8")

            if  'finished' in data_str:
                #time.sleep(10)
                data_obc = json.loads(data_str)

                pub_write = publisher(conf["private_server"],conf["write_port"],'')

                pub_write.publish_write_newblock(data_obc['finished'])
                socket.close()
                context.term()
                break

