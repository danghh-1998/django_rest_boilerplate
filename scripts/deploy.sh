#!/usr/bin/env bash
if [ -d "simple_rest" ]; then
  # shellcheck disable=SC2164
  cd simple_rest
  git pull origin master
else
  git clone "git@gitlab.com:hoanghaidang/simple_rest.git"
fi
