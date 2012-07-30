#!/usr/bin/python
"""
"""
# http://tex.stackexchange.com/questions/22487/create-a-symbol-font-from-svg-symbols

import fontforge
from os import path
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('literatewebfont')
import glob, sys

import optparse
from pprint import pprint, pformat

def get_parser( ):
  parser = optparse.OptionParser( )
  parser.add_option('-o', '--output',
                    default="./fonts",
                    help="Write fonts to OUTPUT")
  parser.add_option('--fontname',
                    default="Font",
                    help="fontforge's font.fontname")
  parser.add_option('--familyname',
                    default="Literate Web",
                    help="fontforge's font.familyname")
  parser.add_option('-g', '--glyphs',
                    default="*.glyph.svg",
                    help="Glob for GLYPHS")
  return parser

def prep_val(val):
  if ' ' in val:
    return "'%s'" % val
  return val

def print_reproducible_run(parser, options, args):
  cmd = parser.prog or args[0]
  args = args[1:]
  cmdline = [ cmd, ]
  for opt in parser.option_list:
    k = opt.dest or opt.get_opt_string( )
    if hasattr(options, k):
      v = getattr(options, k)
      cmdline.append('='.join([ opt.get_opt_string( ), prep_val(v) ]))
  cmdline.extend(args)
  print ' '.join(cmdline)

class WebFont(object):
  def __init__(self, opts, args):
    self.options = opts
    self.args = args

  def collect_glyphs(self, theme):
    search = path.join(theme, self.options.glyphs)
    return glob.glob(search)

  def convert(self, theme):
    file_prefix = path.join(self.options.output, theme)
    # create empty font
    self.font = font = fontforge.font()

    #file_prefix = 'icons'

    # set font names
    font.fontname = self.options.fontname
    font.familyname = self.options.familyname
    font.fullname = ' '.join([ self.options.familyname, self.options.fontname ])

    # import svgs
    files = self.collect_glyphs(theme)
    for f in files:
      self.import_glyph(f)

    #font.generate("fonts/%s.pfb" % file_prefix, flags=["tfm", "afm"]) # type1 with tfm/afm
    #font.generate("fonts/%s.otf" % file_prefix) # opentype
    font.generate("%s.ttf" % file_prefix) # truetype
    font.generate("%s.svg" % file_prefix) # svg
    font.generate("%s.woff" % file_prefix) # svg
    fontforge.printSetup('pdf-file', '%s-preview.pdf' % file_prefix)
    font.printSample('fontdisplay', 14)

  def import_glyph(self, pathname):
    """
    Import an SVG as a single glyph.
    """
    name = path.basename(pathname)
    print name

    code, short = name.split('.')[:2]
    glyph = int('0x' + code, 16)
    char  = unicode(glyph)

    # create a new glyph with the code point i
    glyph = self.font.createChar(glyph, short)

    # import svg file into it
    #glyph.importOutlines("%s.svg" % f)
    glyph.importOutlines(pathname)

    # make the glyph rest on the baseline
    ymin = glyph.boundingBox()[1]
    glyph.transform([1, 0, 0, 1, 0, -ymin])

    # set glyph side bearings, can be any value or even 0
    glyph.left_side_bearing = glyph.right_side_bearing = 10

def main(*args):
  parser = get_parser( )
  (options, args) = parser.parse_args(list(args))
  print_reproducible_run(parser, options, args)
  prog, args = args[0], args[1:]

  font = WebFont(options, args)
  for theme in args:
    font.convert(theme)

if __name__ in [ '__main__' ]:
  main(*sys.argv)

#####
# EOF
