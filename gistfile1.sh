#!/bin/sh

## Requirements
## 1. pdfinfo
## 2. Imagemagick convert
## 3. tesseract

SOURCE=$1

for file in $SOURCE/*;do

  PAGES=$(pdfinfo $file | awk '/Pages:/ { print $2 }')

  for i in $(seq 1 $PAGES); do
    echo "======= $file $i"
    convert -density 300 -depth 8  -gravity south -crop 100x85% $file\[$(($i - 1 ))\] PNG:- | tesseract stdin stdout
  done
done
