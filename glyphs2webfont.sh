#!/bin/bash

python simple.py $*

for theme in $* ; do
  if [[ -d $theme ]] ; then
    ttf2eot "fonts/$theme.ttf" > "fonts/$theme.eot"
    name=$(basename $theme)
    ./glyphs.py -n fonts/glyphs.svg \
      | cut -d' ' -f 2,4 | sed -e "s|^|icon-|g" \
      | ./glyph2css.sh  > css/$name.css

  fi
done

#####
# EOF
