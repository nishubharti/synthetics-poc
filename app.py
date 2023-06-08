#!/usr/bin/env python3
from github import Github
import os
import re
import urllib.parse
from confluent_kafka import Producer

GIT_REPO=os.environ['GIT_REPO']
GIT_TOKEN=os.environ['GIT_TOKEN']
SASL_PASSWORD=os.environ['SASL_PASSWORD']
BOOTSTRAP_SERVER=os.environ['BOOTSTRAP_SERVER']

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

def get_git_repo(git_url,git_token):
   
    parsed_url = urllib.parse.urlparse(git_url)
    hostname=parsed_url.netloc
    regex_comp=re.compile(r"\/tree\/(master|main)\/")
    mo = regex_comp.search(git_url)
    #seperating the git url and the folder path
    folder_path=git_url.split(mo.group())[1]
    updated_git_url=git_url.split(mo.group())[0]
    g = Github(base_url=f'https://{hostname}/api/v3', login_or_token=git_token)
    gitRepo=updated_git_url.split(hostname+'/')[1]
    repo = g.get_repo(gitRepo)

    contents = repo.get_contents(folder_path)

    for content_file in contents:
        if content_file.type == "file":
            p.poll(0)
            file_content = content_file.decoded_content.decode("utf-8")
            print(f"Content of '{content_file.path}':")
            print(file_content)
            p.produce('test-topic', file_content, callback=delivery_report)
            p.flush()
    
def main():
    get_git_repo(GIT_REPO,GIT_TOKEN)
    
if __name__ == '__main__':
    main()