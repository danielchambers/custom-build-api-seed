#!/bin/awk

# run script
#$ awk -f parsedata.awk BMW.csv > json.txt

BEGIN {
  FS = ","
}

{
  if ($0 ~ /^[0-9]{10}/) {
    if ($7 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) {

      print "{\\\"date\\\":\\\"" $1 "\\\", \\\"score\\\":\\\"" $2 "\\\", \\\"domain\\\":\\\"" $3 "\\\", \\\"title\\\":\\\"" $5 "\\\", \\\"author\\\":\\\"" $6 "\\\", \\\"upVote\\\":\\\"" $7 "\\\", \\\"downVote\\\":\\\"" $8 "\\\", \\\"comments\\\":\\\"" $9 "\\\"}"

    }
  }
}

