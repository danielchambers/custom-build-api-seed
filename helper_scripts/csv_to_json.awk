#!/bin/awk

# run script and save output to text file
# awk -f parsedata.awk BMW.csv > json.txt

BEGIN {
  FS = ","
}

{
  if ($0 ~ /^[0-9]{10}/) {
    if ($7 ~ /^[0-9]+$/ && $8 ~ /^[0-9]+$/) {
      printf "{\"date\": \"%s\", \"score\": %s, \"domain\": \"%s\", \"title\": \"%s\", \"author\": \"%s\", \"upVote\": %s, \"downVote\": %s, \"comments\": %s}\n", $1,$2,$3,$5,$6,$7,$8,$9
    }
  }
}

