#!/bin/bash

sudo apt-get install $(grep -vE "^\s*#" requirements.txt  | tr "\n" " ")
