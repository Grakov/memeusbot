#!/bin/bash

ELASTICSEARCH_PATH=/usr/share/elasticsearch
HUNSPELL_PATH=$ELASTICSEARCH_PATH/config/hunspell/ru_RU

if [[ ! -d "$HUNSPELL_PATH" ]]; then
  mkdir -p $HUNSPELL_PATH
  cp ru_RU.* $HUNSPELL_PATH
fi

elasticsearch