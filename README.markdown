
# Literate Web Font

## TL;DR
This is a literate programming jekyll site to used to develop fonts on
github with a special focus on ding bat webfonts.

## Usage

### Install

    git clone git@github.com:bewest/literatewebfont.git
    cd literatewebfont

### Create a naive webfont

    # glob input from glyphs/ prefix output to fonts/glyphs.
    ./glyphs2webfont.sh glyphs

This will generate a set of css3 webfonts named:

  * `fonts/glyphs.woff`
  * `fonts/glyphs.eot`
  * `fonts/glyphs.svg`
  * `fonts/glyphs.ttf`

by importing individual SVG images, `1000px x 1000px`
from images found by globbing for `glyphs/*.glyphs.svg`.

    # This will generate a set of css3 webfonts named `foo.woff` in
    # `fonts/foo.woff` ...  globbing for `foo/*.glyphs.svg`.
    ./glyphs2webfont.sh foo

The script wraps simple.py which will allow you to customize what
happens through some commandline flags.

### Extract glyphs

    # This will extract each glyph found in a font to an svg vector in
    # the `awesome` directory.
    ./glyphs.py -p awesome/ ../Font-Awesome/font/fontawesome-webfont.ttf

### Rebuild a font

    # will create font/awesome.[woff|eot] et al.
    ./glyphs2webfont.sh awesome

### Preview your new icons/font
If you run: `jekyll --site --auto` you can preview your new font by
visiting http://localhost:4000/.  You may have to edit the html and
css to remap your glyphs.
TODO: automate stubs for css and html that can be included from a
generated template.


## Problem
You have a bunch of symbols deployable as separate images, often used
throughout a site.  The excellent tools available to us have
previously provided CSS sprites, which allow clever authors to compose
often used symbols into a single sprite by fine tuning the clipping
area controlling the visible viewport.  You may have a solution that
programatically manages these using some vector based format.  Given
our manifest of symbols it'd be nice if there was a way to easily
create a ding-bat web-font to make these symbols usable and
rescalable.

## Idea
The idea is to have suite of tools that allows you to clone the repo,
run rake/make and compile a new font from a manifest of glyphs
maintained in ./glyphs.

The ./glyphs directory should contain svg images named 
  **hexcode**.**shorthand**.glyph.svg

Each glyph will be included in the font and mapped to it's
unicode code to it's shorthand name in a css file.  Immediate
development is in lib.hello.py.

Here are the glyph specs:
> By default, fontforge glyph dimension box is 1000 x 1000 postscript
> units.
> The baseline line is set at 0pt.
> ascenders goes up to 800pt
> and descender down to 200pt.
> 
> In Inkscape, create a new document
> In document properties, set all your units in inkscape in pixels (px).
> Set the document dimension to 1000px x 1000px
> Set an horizontal guide at 200px
http://ospublish.constantvzw.org/tools/import-inkscape-in-fontforge

The resulting fonts are placed in `./fonts`.

It's possible that this could be combined with a fancy js svg editor
to allow users to edit glyphs in their browser, save changes to their
local disk, compile and upload the new font.

Glyph mappings could be from U+F0000 to U+FFFFD
http://en.wikipedia.org/wiki/Private_Use_(Unicode)#Private_Use_Areas

We can re-use bootstrap's mappings.

## Resources 

  * http://www.w3.org/TR/css3-fonts/
  * http://fontforge.sourceforge.net/python.html
  * http://tex.stackexchange.com/questions/22487/create-a-symbol-font-from-svg-symbols
  * http://code.google.com/p/googlefontdirectory/wiki/HowToGenerateWebNativeFontsWithFontForge
  * http://ospublish.constantvzw.org/tools/import-inkscape-in-fontforge
  * http://scripts.sil.org/cms/scripts/page.php?item_id=IWS-Chapter08#CharacterToGlyphMapping
  * http://old.nabble.com/Fontforge-webfonts-generate-script-td32128949.html
  * https://github.com/zoltan-dulac/css3FontConverter
  * http://www.useragentman.com/blog/2011/02/20/converting-font-face-fonts-quickly-in-any-os/
  * The python tests are useful:
  * http://fontforge.git.sourceforge.net/git/gitweb.cgi?p=fontforge/fontforge;a=tree;f=test;hb=HEAD
  * http://fontforge.sourceforge.net/importexample.html
  * http://mashable.com/2011/12/01/how-web-fonts-are-created/
  * http://fontforge.sourceforge.net/scripting-tutorial.html
  * http://fontforge.sourceforge.net/scripting.html#Example
  * http://fontforge.sourceforge.net/python.html#validation-state
  * http://fontforge.sourceforge.net/scripting-alpha.html#Import
  * http://fontforge.git.sourceforge.net/git/gitweb.cgi?p=fontforge/fontforge;a=blob;f=test/test1007.py;h=08efe56e199786c34f19247fb709737c2566de50;hb=HEAD
  * https://github.com/Heydon/Community-Icon-Font - useful single
    glyph here.
  * https://github.com/FortAwesome/Font-Awesome/
  * http://cleversomeday.wordpress.com/2010/02/09/inkscape-dings/
  * http://css-tricks.com/html-for-icon-font-usage/
  * http://en.wikipedia.org/wiki/Private_Use_(Unicode)#Private_Use_Areas
  * https://github.com/Keyamoon/IcoMoon--limited-
  * https://github.com/bernerdschaefer/ttf2eot/blob/master/lib/ttf2eot.rb
    - Could not get this one to work. LoadErrors
  * https://github.com/greyfont/ttf2eot
  * http://www.kirsle.net/wizards/ttf2eot.cgi#restrictions
  * https://github.com/simi/reot
  * Consider testing and then using as a fall back.
    http://www.kirsle.net/wizards/ttf2eot.cgi#restrictions

The python support looks more than sufficient to inspect a config for
some options (hardcoded), use a directory of glyphs to create a bunch
of symbols into a webfont.  Since the results are viewable in HTML, a
simple tool to update results would be nice.

## TODO
Some option parsing and a manifest/mapping mechanism would go a
long way.

Demo pages to point and demo the new fonts.  Some js to audit and edit
glyphs would be nice.

## Requirements

The excllent jekyll et al, fontforge, python, ttf2eot

Right now it's easier to develop with fontforge installed as a python
plugin rather than the other way around, since this allows logging
what we are doing etc...

### Ubuntu and friends
    sudo apt-get install python-fontforge

I couldn't find ttf2eot in my distribution channels, so I compiled it
from greyfront's github repo.  https://github.com/greyfont/ttf2eot
Download it, do it.  Here:

    git clone git://github.com/greyfont/ttf2eot.git
    cd ttf2eot
    make
    cp ttf2eot ~/bin

If only the last step fails, `mkdir ~/bin` and add
`export PATH=$PATH:~/bin/` to your profile.

### MAC OS/X and brew
I have not tried this:

    # https://github.com/mxcl/homebrew/issues/4689
    brew install fontforge
    brew install ttf2eot

