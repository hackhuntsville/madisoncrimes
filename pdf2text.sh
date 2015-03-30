#!/bin/sh

## Requirements
## 1. pdftotext from poppler-utils

SOURCE=$1
DEST_DIR=tmp-pdf2Text

if [ -d "$DEST_DIR" ]; then
  rmdir $DEST_DIR
fi

mkdir $DEST_DIR

for file in $SOURCE/*;do

  # get the basename of file
  #fname=${file##*[/|\\]}
  fname=$(basename $file)
 
  # convert to text keeping the layout.
  echo "pdftotext $file $DEST_DIR/$fname.txt"
  pdftotext -layout -nopgbrk $file $DEST_DIR/$fname.txt

done

cat $DEST_DIR/*.txt > madison_crimes_converted.text

# remove the tmp dir. comment following line, if needed to debug. 
rmdir $DEST_DIR
