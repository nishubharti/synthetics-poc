#!/usr/bin/env python3
from confluent_kafka import Consumer
import os

BOOTSTRAP_SERVER=os.environ['BOOTSTRAP_SERVER']

def main():
    c = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVER,
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest',
    })

    c.subscribe(['test-topic'])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))
            
    except KeyboardInterrupt:
        pass

    c.close()
    
if __name__ == '__main__':
    main()
