from gub import misc
from gub import target

class LilyPad (target.AutoBuild):
    source = 'http://lilypond.org/downloads/gub-sources/lilypad/lilypad-0.1.3.0-src.tar.xz'
    dependencies = [ 'tools::automake', 'tools::xzutils' ]
    destdir_install_broken = True
    license_files = ['']

Lilypad = LilyPad
