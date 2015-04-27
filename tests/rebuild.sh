#!/bin/bash

# Cache images in circleci
mkdir -p ~/docker

FAILED=()

for DIR in $(find . -maxdepth 1 -type d -printf '%P\n'); do
  # image names must be lowercased
  IMAGE_NAME=`echo $DIR | tr '[:upper:]' '[:lower:]'`
  if [[ -e ~/docker/$IMAGE_NAME.tar ]]; then
    echo "Found cached $IMAGE_NAME image"
    docker load -i ~/docker/$IMAGE_NAME.tar
  else
    echo "Rebuilding $IMAGE_NAME"
    docker build -t fedora/$IMAGE_NAME $DIR; ret=$?
    if [[ $ret -ne 0 ]]; then FAILED+=($IMAGE_NAME); fi
    docker save "fedora/$IMAGE_NAME" > ~/docker/$IMAGE_NAME.tar
  fi
done

if [[ ${$FAILED[@]} -e 0 ]]; then
  echo "All images were built"
  exit 0
else
  echo "The following images failed to build:"
  for (( i=0; i<${$FAILED[@]}; i++ )); do
    echo ${FAILED[$i]}
  done
fi
