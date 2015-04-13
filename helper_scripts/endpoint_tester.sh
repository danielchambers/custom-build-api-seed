#!/bin/bash

# test GET, POST, and PUT endpoints

url=$1
total_insertions=$2

echo "Please enter your choice: "
menu=("GET All Records" "GET Record By ID" "POST Record" "PUT Record", "Populate Database")
select opt in "${menu[@]}"
do
  case "${opt}" in
    "GET All Records")
      echo " "
      echo "GET: All Records"
      curl "${url}"
      ;;
    "GET Record By ID")
      echo " "
      echo "GET: Record By ID"
      echo -n "Record ID: "
      read record_id
      curl "${url}${record_id}"
      ;;
    "POST Record")
      echo " "
      echo "POST: Create Record"
      echo -n "Record Name: "
      read record_id
      curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"${record_id}\"}" "${url}"
      ;;
    "PUT Record")
      echo " "
      echo "PUT: Update Record"
      echo -n "Record Name: "
      read record_name
      echo -n "Record ID: "
      read record_id
      curl -X PUT -H "Content-Type: application/json" -d "{\"name\":\"${record_name}\"}" "${url}${record_id}"
      ;;
    "Populate Database")
      echo " "
      echo "POST: Populate Database"
      bash add.sh ${total_insertions} "${url}"
      ;;
    *)
      break
      ;;
  esac
done
