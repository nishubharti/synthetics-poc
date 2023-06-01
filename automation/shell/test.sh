#!/bin/bash
export API_KEY=$1
export SOURCE_CODE=$2
export GIT_REPO=$3
export GIT_TOKEN=$4
export SASL_PASSWORD=$5
export BOOTSTRAP_SERVER=$6

echo "Login into IBM Cloud account"
ibmcloud login --apikey ${API_KEY} -r us-south -g Default -a=cloud.ibm.com

echo "creating a Code Engine project"
ibmcloud ce project create -n test-Synthetics-poc

echo "selecting a Code Engine project"
ibmcloud ce project select -n test-Synthetics-poc

echo "creating a job in Code Engine project"
ibmcloud ce job create --name test-syn-job --build-source ${SOURCE_CODE} -e GIT_REPO=${GIT_REPO} -e GIT_TOKEN=${GIT_TOKEN} -e SASL_PASSWORD=${SASL_PASSWORD} -e BOOTSTRAP_SERVER=${BOOTSTRAP_SERVER}

echo "get a job in Code Engine project"
ibmcloud ce job get --name test-syn-job

echo "creating a cron event"
ibmcloud ce sub cron create --name mycronevent --destination-type job --destination test-syn-job --schedule '0 0 * * *'

# echo "submit the job"
# ibmcloud ce jobrun submit --job my-syn-job2