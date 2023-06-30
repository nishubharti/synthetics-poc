#!/usr/bin/env python3

from github import Github
import os
import re
import json
import urllib.parse
from confluent_kafka import Producer

GIT_REPO = os.environ['GIT_REPO']
GIT_TOKEN = os.environ['GIT_TOKEN']
SASL_PASSWORD = os.environ['SASL_PASSWORD']
BOOTSTRAP_SERVER = os.environ['BOOTSTRAP_SERVER']
PATHS = os.environ['PATHS']

p = Producer({'bootstrap.servers': BOOTSTRAP_SERVER,
              'sasl.username': 'token',
              'sasl.password': SASL_PASSWORD,
              'security.protocol': 'SASL_SSL',
              'sasl.mechanism': 'PLAIN'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]\n{}'.format(msg.topic(), msg.offset(), msg.value()))

def get_git_repo(git_url, git_token, paths):
    parsed_url = urllib.parse.urlparse(git_url)
    hostname = parsed_url.netloc
    g = Github(base_url=f'https://{hostname}/api/v3', login_or_token=git_token)
    gitRepo = git_url.split(hostname+'/')[1]
    repo = g.get_repo(gitRepo)

    payloads = []
    manifest_file = None
    labels = {}  # Initialize an empty labels dictionary

    for file in paths.split(','):
        contents = repo.get_contents(file)
        if contents.type == "file":
            if file.endswith('.json'):
                manifest_path = file.rsplit('/', 1)[0] + '/Cnf'
                manifest_file = repo.get_contents(manifest_path)
                p.poll(0)
                data = json.loads(contents.decoded_content.decode('utf8').replace("'", '"'))

                if 'api' in file:
                    json_name = contents.name.replace('.json', '.js')
                    json_file = file.replace(contents.name, json_name)
                    json_contents = repo.get_contents(json_file)
                    data['script'] = json_contents.decoded_content.decode('utf8')

                msg_struct = {
                    "id": contents.name,
                    "payload": data,
                }
                payloads.append(msg_struct)
                print('Message:', msg_struct)  # Print the message content

    if manifest_file:
        manifest_data = json.loads(manifest_file.decoded_content.decode('utf8').replace("'", '"'))
        labels = manifest_data
        if labels:
            for payload in payloads:
                payload['label'] = labels
                print('Message:', payload)  # Print the message content

    for payload in payloads:
        event_payload = {
            "id": payload['id'],
            "label": payload['label'],
            "payload": payload['payload'],
        }
        event_pay = json.dumps(event_payload)
        p.produce('test-topic', event_pay, callback=delivery_report)
        p.poll(0)

    p.flush()

def main():
    get_git_repo(GIT_REPO, GIT_TOKEN, PATHS)

if __name__ == '__main__':
    main()