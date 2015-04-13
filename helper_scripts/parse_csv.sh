#!/bin/bash

# useage: bash ./helper_scripts/parse_csv.sh

if [ -f ./data/json.txt ]
then
 echo "json.txt found"
else
  # convert csv data to json data
  awk -f ./helper_scripts/csv_to_json.awk ./data/BMW.csv > ./data/json.txt
fi

if [ $# -ne 1 ]
then
  echo "please provide the url to post to"
  exit 1
else
  url=$1
  while read line
  do
    curl -X POST -H "Content-Type: application/json" -d "${line}" "${url}"
  done < ./data/json.txt
  echo "done"
fi
