#!/bin/bash

# bash script_file.sh 30 http://127.0.0.1:5000/
# populate database using names from fakenamegenerator.com

total_iterations=$1
server=$2
loop_counter=0

fakenamegenerator () {
  host="Host: www.fakenamegenerator.com"
  referer="Referer: http://www.fakenamegenerator.com/"
  user_agent="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36"

  curl -s -H "${host}" -H "${referer}" -H "${user_agent}" http://www.fakenamegenerator.com/gen-random-us-us.php
}

fakenamegenerator_name () {
  echo "${fakenamegenerator_html}" | gawk '{
    match($0, /<h3>(\w+)\s\w+\.\s(\w+)<\/h3>/, name);

    print name[1]
  }'
}

while [ "${loop_counter}" -lt "${total_iterations}" ]
do
  fakenamegenerator_html=$(fakenamegenerator)
  firstname=$(echo $(fakenamegenerator_name) | tr -d '[:space:]')

  curl -s -H "Content-Type: application/json" -X POST -d "{\"name\":\"${firstname}\"}" "${server}"
done
