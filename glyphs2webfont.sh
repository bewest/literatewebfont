#!/bin/bash

python simple.py $*

for theme in $* ; do
  if [[ -d $theme ]] ; then
    ttf2eot "fonts/$theme.ttf" > "fonts/$theme.eot"
    name=$(basename $theme)
    # potentially smarter version of this would use xpath+sass
    # function to generate a list of these to iterate over.  in any
    # case, list all the glyphs, and generate a css stanza that
    # generates content using that glyph.
    ./glyphs.py -n fonts/$theme.svg \
      | cut -d' ' -f 2,4 | sed -e "s|^|icon-|g" \
      | ./glyph2css.sh  > css/$name.css

  fi
done

#####
# EOF
