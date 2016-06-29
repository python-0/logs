#!/bin/bash

opration=$1

function _doo() {
  c=`docker ps |grep -w logs_test|wc -l`
  if [ $c -eq 0 ]; then
    docker run \
        --name=logs_test \
        -h node2 \
        -d \
        -v $(pwd)/test/id_rsa.pub:/root/\.ssh/authorized_keys:ro \
        -v $(pwd)/test/catalina.out:/opt/catalina.out:ro \
        registry.aliyuncs.com/xiaoer_docker/python2.7
  fi
  
  exec docker run \
      --name=logs_dev \
      -h logs-dev \
      --rm \
      --link logs_test:node2 \
      -it \
      -v $(pwd)/test/id_rsa:/root/\.ssh/id_rsa:ro \
      -v $(pwd):/app \
      -w /app \
      -p 5000:5000 \
      logs_dev:latest bash
}

function doo() {
  c=`docker ps |grep -w logs_dev |wc -l`
  if [ $c -eq 1 ]; then
    exec docker exec -it logs_dev bash
  else
    _doo
  fi
}

function init() {
  docker run \
    --name=logs_init \
    -v $(pwd):/app \
    -w /app \
    registry.aliyuncs.com/xiaoer_docker/python2.7 sh -c "pip install -r requment.txt"
  docker commit logs_init logs_dev:latest
  docker rm -f logs_init
}

function append(){
  docker run \
    --name=logs_append \
    -v $(pwd):/app \
    -w /app \
    logs_dev:latest sh -c "pip install -r requment.txt"
  docker commit logs_append logs_dev:latest
  docker rm -f logs_append
}


case $opration in
  init)
    init
    ;;
  append)
    append
    ;;
  do)
    doo
    ;;
esac
