#!/usr/bin/env bash
eval $(ssh-agent -s)
if [ -d "rest_boilerplate" ]; then
  cd rest_boilerplate
  git pull origin master
else
  git clone "git@gitlab.com:hoanghaidang/rest_boilerplate.git"
fi
