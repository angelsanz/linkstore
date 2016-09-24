#!/usr/bin/env bash

set -e

docker build --tag linkstore-dev .

docker run --rm --interactive --tty --volume /code/linkstore.egg-info --volume $(pwd):/code linkstore-dev scripts/test.bash
