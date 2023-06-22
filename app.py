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
PATHS=os.environ['PATHS']

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
    file_paths=paths.split(',')
    for file in file_paths:
        contents = repo.get_contents(file)
        if contents.type == "file":
            p.poll(0)
            data = json.loads(contents.decoded_content.decode('utf8').replace("'", '"'))
            #In progress
            if 'api' in file:
                json_name=contents.name.replace('.json','.js')
                json_file=file.replace(contents.name,json_name)
                contents = repo.get_contents(json_file)
                data['script']=contents.decoded_content.decode('utf8')
            
            msg_struct={
                "id": contents.name,
                "label": "initiated",
                "payload": data,
            }
            payloads.append(msg_struct)
        
    event_pay=json.dumps(payloads)    
    p.produce('test-topic', event_pay, callback=delivery_report)
    p.flush()
    
def main():
    get_git_repo(GIT_REPO,GIT_TOKEN,PATHS)
    
if __name__ == '__main__':
    main()