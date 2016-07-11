#!/bin/bash

OPT=$1

function doo() {
  c=`docker ps |grep -w logs_dev |wc -l`
  if [ $c -eq 1 ]; then
    exec docker exec -it logs_dev bash
  else
    docker rm logs_dev
    exec docker run \
      --name=logs_dev \
      -h logs-dev \
      --rm \
      --link logs_test:node2 \
      --link logs_mysql:mysql \
      --link logs_redis:redis \
      -it \
      -v $(pwd)/test/id_rsa:/root/\.ssh/id_rsa:ro \
      -v $(pwd):/app \
      -w /app \
      -p 5000:5000 \
      logs_dev:latest bash
  fi
}

function init() {
  case $1 in
    dev)
      docker pull registry.aliyuncs.com/xiaoer_docker/python2.7
      docker run \
        --name=logs_init \
        -v $(pwd):/app \
        -w /app \
        registry.aliyuncs.com/xiaoer_docker/python2.7 sh -c "pip install -r requment.txt"
      docker commit logs_init logs_dev:latest
      docker rm -f logs_init
      ;;
    mysql)
      docker rm -f logs_mysql
      docker run \
        --name logs_mysql \
        -h logs-mysql \
        -d \
        -p 3306:3306 \
        -v $(pwd)/test/mysql/db:/docker-entrypoint-initdb.d:ro \
        -v $(pwd)/test/mysql/conf:/etc/mysql/conf.d:ro \
        -e MYSQL_ROOT_PASSWORD=123456 \
        -e MYSQL_DATABASE=logs  \
        -e MYSQL_USER=logs \
        -e MYSQL_PASSWORD=logs \
        mysql:5.6
      ;;
    redis)
      docker rm -f logs_redis
      docker run \
        --name logs_redis\
        -h logs-redis\
        -d \
        -p 6379:6379 \
        redis
      ;;
    test)
      docker rm -f logs_test
      docker run \
        --name=logs_test \
        -h node2 \
        -d \
        -v $(pwd)/test/id_rsa.pub:/root/\.ssh/authorized_keys:ro \
        -v $(pwd)/test/catalina.out:/opt/catalina.out:ro \
        registry.aliyuncs.com/xiaoer_docker/python2.7
      ;;
    all)
      init dev
      init mysql
      init redis
      init test
      ;;
  esac
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

case $OPT in
  init)
    init $2
    ;;
  append)
    append
    ;;
  export)
    docker exec logs_mysql sh -c 'mysqldump -p"$MYSQL_ROOT_PASSWORD" logs' > $(pwd)/test/mysql/db/logs.sql
    ;;
  do)
    doo
    ;;
esac
