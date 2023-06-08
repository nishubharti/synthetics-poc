#!/bin/bash
export API_KEY=$1
export SOURCE_CODE=$2
export GIT_REPO=$3
export GIT_TOKEN=$4
export SASL_PASSWORD=$5
export BOOTSTRAP_SERVER=$6

# echo "Login into IBM Cloud account"
# ibmcloud login --apikey ${API_KEY} -r us-south -g Default -a=cloud.ibm.com

echo "creating a Code Engine project"
ibmcloud ce project create -n test-Synthetics-poc2

echo "selecting a Code Engine project"
ibmcloud ce project select -n test-Synthetics-poc2

echo "cloning a git repo in tmp folder"
basename=$(basename $GIT_REPO)
filename=${basename%.*}
echo ${filename}
git clone ${GIT_REPO}
cd ${filename}

ref_name=$(git branch -l master main | sed 's/^* //')
echo "ref name is" ${ref_name} 

value=$(echo `cat configs.json | jq -c '.[]'`)

for item in ${value[@]}; do
    name=$(echo $item | jq '.name' | tr -d '"')
    sch=$(echo $item | jq '.repeat' | tr -d '"')
    path=$(echo $item | jq '.test_group_paths[0]' | tr -d '"')
    echo ${name}
    echo ${sch}
    echo ${path}

    if [[ ${sch} == *m ]]; then
        interval=$(echo ${sch} | sed 's/[^0-9]//g')
        schedule="*/${interval} * * * * "
    elif [[ ${sch} == *h ]]; then
        interval=$(echo ${sch} | sed 's/[^0-9]//g')
        schedule="0 */${interval} * * *"
    elif [[ ${sch} == *d ]]; then
        interval=$(echo ${sch} | sed 's/[^0-9]//g')
        schedule="0 0 */${interval} * *"
    else
        echo "Invalid repeat value: ${sch}"
        exit 1
    fi
    echo "Cron schedule: $schedule"
    
    MOD_GIT_REPO=${GIT_REPO}/tree/${ref_name}/${path}
    echo "new git repo is " ${MOD_GIT_REPO}

    # echo "creating a job in Code Engine project"
    ibmcloud ce job create --name job-${name} --build-source ${SOURCE_CODE} -e GIT_REPO=${MOD_GIT_REPO} -e GIT_TOKEN=${GIT_TOKEN} -e SASL_PASSWORD=${SASL_PASSWORD} -e BOOTSTRAP_SERVER=${BOOTSTRAP_SERVER}

    # echo "get a job in Code Engine project"
    ibmcloud ce job get --name job-${name}

    # echo "creating a cron event"
    ibmcloud ce sub cron create --name cron-${name} --destination-type job --destination job-${name} --schedule "${schedule}"


done

# echo "creating a job in Code Engine project"
# ibmcloud ce job create --name test-syn-job --build-source ${SOURCE_CODE} -e GIT_REPO=${GIT_REPO} -e GIT_TOKEN=${GIT_TOKEN} -e SASL_PASSWORD=${SASL_PASSWORD} -e BOOTSTRAP_SERVER=${BOOTSTRAP_SERVER}

# echo "get a job in Code Engine project"
# ibmcloud ce job get --name test-syn-job

# echo "creating a cron event"
# ibmcloud ce sub cron create --name mycronevent --destination-type job --destination test-syn-job --schedule '0 0 * * *'

# echo "submit the job"
# ibmcloud ce jobrun submit --job my-syn-job2
cd ..
#delete the cloned repo
rm -rf ${filename}