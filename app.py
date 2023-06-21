#!/usr/bin/env python3
from github import Github
import os
import re
import json
import urllib.parse
from confluent_kafka import Producer

GIT_REPO=os.environ['GIT_REPO']
GIT_TOKEN=os.environ['GIT_TOKEN']
SASL_PASSWORD=os.environ['SASL_PASSWORD']
BOOTSTRAP_SERVER=os.environ['BOOTSTRAP_SERVER']
print("type here",type(os.environ['PATHS']))
PATHS=json.loads(os.environ['PATHS'])

p = Producer({'bootstrap.servers': BOOTSTRAP_SERVER,
              'sasl.username': 'token',
              'sasl.password': SASL_PASSWORD,
              'security.protocol': 'SASL_SSL',
              'sasl.mechanism': 'PLAIN'
               })

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.offset(),msg.partition()))

def get_git_repo(git_url,git_token,paths):
   
    parsed_url = urllib.parse.urlparse(git_url)
    hostname=parsed_url.netloc
    g = Github(base_url=f'https://{hostname}/api/v3', login_or_token=git_token)
    gitRepo=git_url.split(hostname+'/')[1]
    repo = g.get_repo(gitRepo)
        
    payloads=[]
    for file in paths:
        folder_path=file
        contents = repo.get_contents(folder_path)
        if contents.type == "file":
            p.poll(0)
            file_content = contents.decoded_content.decode("utf-8")
            msg_struct={
                "id": contents.name,
                "label": "initiated",
                "payload": file_content
            }
            payloads.append(msg_struct)
            
    print("msg structure here is",msg_struct)
    # p.produce('test-topic', str(msg_struct), callback=delivery_report)
    # p.flush()
    
def main():
    get_git_repo(GIT_REPO,GIT_TOKEN,PATHS)
    
if __name__ == '__main__':
    main()