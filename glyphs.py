#!/usr/bin/python

"""
Export glyphs from a font file into a theme directory with each glyph
saved as its own svg file.
"""

import fontforge
import sys, os, optparse

from os import path

from pprint import pprint, pformat

def get_parser( ):
  parser = optparse.OptionParser( )
  parser.add_option('-n', '--noop',
                    default=False,
                    action='store_true',
                    help="Write glyphs to this directory.")
  parser.add_option('-p', '--prefix',
                    default="themes",
                    help="Write glyphs to this directory.")
  parser.add_option('-s', '--suffix',
                    default="glyph.svg",
                    help="Use this suffix when writing glyphs.")
  return parser


class Inspector(object):
  def __init__(self, options, args):
    self.options = options
    self.args = args

  def run(self):
    for font in self.args:
      self.inspect(font)

  def inspect(self, name):
    self.font = font = fontforge.open(name)
    for glyph in font.glyphs('encoding'):
      if glyph.unicode > 0:
        self.rip_glyph(glyph)

  def rip_glyph(self, glyph):
    prefix = self.options.prefix
    suffix = self.options.suffix
    code = "%04x" % glyph.unicode
    short= glyph.glyphname
    name = '.'.join([code, short, suffix])
    output = path.join(prefix, name)
    print output, glyph.glyphname, 'code', "%04x" % glyph.unicode
    if not self.options.noop:
      glyph.export(output)

def main(*args):
  parser = get_parser( )
  (options, args) = parser.parse_args(list(args))
  prog, args = args[0], args[1:]

  app = Inspector(options, args)
  app.run( )

if '__main__' == __name__:
  main(*sys.argv)

#####
# EOF
