#!/usr/bin/python


import fontforge
import sys

def inspect_glyphs(font):
  for glyph in font.glyphs("encoding"):
    print glyph


def inspect_font_file(name):
  font = fontforge.open(name)
  inspect_glyphs(font)


if '__main__' in [ __name__ ]:
  for name in sys.argv[1:]:
    print name
    inspect_font_file(name)

#####
# EOF
