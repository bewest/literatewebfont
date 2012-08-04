#!/bin/bash


function generate_content () {
LABEL=$1
GLYPH=$2
cat <<EOT
.${LABEL}:before { content: "\\${GLYPH}"; }
EOT

}
if [ -t 0 ]; then
  generate_content $1 $2
else
  while read label glyph; do
    generate_content $label $glyph
  done
fi

#####
# EOF
