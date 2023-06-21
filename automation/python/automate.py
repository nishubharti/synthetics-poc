#!/usr/bin/env python3
import os
import sys
import git
import json

API_KEY=sys.argv[1]
SOURCE_CODE=sys.argv[2]
GIT_REPO=sys.argv[3]
GIT_TOKEN=sys.argv[4]
SASL_PASSWORD=sys.argv[5]
BOOTSTRAP_SERVER=sys.argv[6]

print("logging into ibm cloud")
os.system("ibmcloud login --apikey={0} -r us-south -g Default -a=cloud.ibm.com".format(API_KEY))

print("creating a Code Engine project")
os.system("ibmcloud ce project create -n test-Synthetics-poc2")

print("selecting a Code Engine project")
os.system("ibmcloud ce project select -n test-Synthetics-poc2")

print("cloning the git repository in tmp")
git.Repo.clone_from(GIT_REPO,'./tmp')

# Opening JSON file
f = open('tmp/configs.json')
  
# returns JSON object as # a dictionary
data = json.load(f)
  
# Iterating through the json list
for i in data:
    sch=i
    Github=data[i]['Github']
    paths=data[i]['paths']
    
    if 'm' in sch:
        interval=sch.split('m')[0]
        schedule="*/{0} * * * * ".format(interval)
    elif 'h' in sch:
        interval=sch.split('h')[0]
        schedule="0 */{0} * * *".format(interval)
    elif 'd' in sch:
        interval=sch.split('d')[0]
        schedule="0 0 */{0} * *".format(interval)
    else:
        print("Invalid repeat value: ",sch)
        exit
        
    print("creating a job in Code Engine project")
    os.system("ibmcloud ce job create --name=job-{0} --build-source={1} -e GIT_REPO={2} -e GIT_TOKEN={3} -e SASL_PASSWORD={4} -e BOOTSTRAP_SERVER={5} -e PATHS='{6}'".format(sch,SOURCE_CODE,GIT_REPO,GIT_TOKEN,SASL_PASSWORD,BOOTSTRAP_SERVER,paths))

    print("creating a cron event")
    os.system("ibmcloud ce sub cron create --name=cron-{0} --destination-type=job --destination=job-{0} --schedule='{1}'".format(sch,schedule))
   
    print("creation of the jon is done for job-",{sch})
    print("*****************")
    print("*****************")
    print("*****************")
    print("*****************")
    print("")
    
    
f.close()
os.system("rm -rf tmp")


















