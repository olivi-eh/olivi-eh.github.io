#!/bin/sh

set -e

rm -Rf out/

python3 md2html.py

for file in out/*.html
do
    filename=$(basename "$file" .html)

    if [ "$filename" = "index" ]; then
        continue
    fi

    mkdir -p "out/$filename"
    mv "$file" "out/$filename/index.html"
done

cp -R static/ out/
cp 404.html CNAME robots.txt out/
