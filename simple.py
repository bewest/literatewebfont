# http://tex.stackexchange.com/questions/22487/create-a-symbol-font-from-svg-symbols

import fontforge
from os import path
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('literatewebfont')
import glob

# create empty font
font = fontforge.font()

output_file = 'icons'

# set font names
font.fontname = "LiterateWebFont"
font.fullname = "Literate Web Font"
font.familyname = "LiterateWeb"


# import svgs
files = glob.glob('./glyphs/*.glyph.svg')
for f in files:
    name = path.basename(f)
    # print name
    code, short = name.split('.')[:2]
    glyph = int('0x' + code, 16)
    char  = unicode(glyph)

    # create a new glyph with the code point i
    glyph = font.createChar(glyph, name)

    # import svg file into it
    #glyph.importOutlines("%s.svg" % f)
    glyph.importOutlines(f)

    # make the glyph rest on the baseline
    ymin = glyph.boundingBox()[1]
    glyph.transform([1, 0, 0, 1, 0, -ymin])

    # set glyph side bearings, can be any value or even 0
    glyph.left_side_bearing = glyph.right_side_bearing = 10

font.generate("fonts/%s.pfb" % output_file, flags=["tfm", "afm"]) # type1 with tfm/afm
font.generate("fonts/%s.otf" % output_file) # opentype
font.generate("fonts/%s.ttf" % output_file) # truetype
font.generate("fonts/%s.svg" % output_file) # svg
font.generate("fonts/%s.woff" % output_file) # svg
fontforge.printSetup('pdf-file', 'fonts/%s-preview.pdf' % output_file)
font.printSample('fontdisplay', 14)

#####
# EOF
