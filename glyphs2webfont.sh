#!/bin/bash

python simple.py $*

for theme in $* ; do
  if [[ -d $theme ]] ; then
    echo ttf2eot "fonts/$theme" > "fonts/$theme.eot"
  fi
done

#####
# EOF
