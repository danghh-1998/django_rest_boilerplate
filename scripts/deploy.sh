#!/usr/bin/env bash
if [ -d "simple_rest" ]; then
  cd simple_rest
  git pull origin master
else
  git clone "git@gitlab.com:hoanghaidang/simple_rest.git"
fi
