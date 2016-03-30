#!/bin/bash

WHITE=0
BLACK=0
STALE=0
FIFTY=0
REPEAT=0
RETVAL=0

while :
do
  sleep 2
  python interface.py
  RETVAL=$?
  echo "return code $RETVAL"
  if [[ $RETVAL -eq 1 ]]
  then 
    WHITE=$((WHITE+1))
  elif [[ $RETVAL -eq 2 ]]
  then
    BLACK=$((BLACK+1))
  elif [[ $RETVAL -eq 3 ]]  
  then
    STALE=$((STALE+1))
  elif [[ $RETVAL -eq 4 ]]  
  then
    FIFTY=$((FIFTY+1))
  elif [[ $RETVAL -eq 5 ]]  
  then
    REPEAT=$((REPEAT+1))
  else
    echo "UNEXPECTED ERROR CODE: $RETVAL"
    echo "white: $WHITE black: $BLACK stale: $STALE fifty: $FIFTY repeat: $REPEAT "
    exit 1
  fi

  echo "white: $WHITE black: $BLACK stale: $STALE fifty: $FIFTY repeat: $REPEAT "
done
