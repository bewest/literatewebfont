# http://tex.stackexchange.com/questions/22487/create-a-symbol-font-from-svg-symbols

import fontforge

# create empty font
font = fontforge.font()

# set font names
font.fontname = "FooBar"
font.fullname = "Foo Bar"
font.familyname = "Foo Bar"


# import svgs
files = [ 'glyphs/']
for i in range(1, 701):
    # create a new glyph with the code point i
    glyph = font.createChar(i)

    # import svg file into it
    glyph.importOutlines("%s.svg" %i)

    # make the glyph rest on the baseline
    ymin = glyph.boundingBox()[1]
    glyph.transform([1, 0, 0, 1, 0, -ymin])

    # set glyph side bearings, can be any value or even 0
    glyph.left_side_bearing = glyph.right_side_bearing = 10

font.generate("foobar.pfb", flags=["tfm", "afm"]) # type1 with tfm/afm
font.generate("foobar.otf") # opentype
font.generate("foobar.ttf") # truetype

#####
# EOF
