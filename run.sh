#!/bin/sh

set -e

python3 -m http.server 8082 --directory out/
