from gub import tools
from gub import build

class Fonts_urw_core35 (build.BinaryBuild):
    # http://git.ghostscript.com/?p=urw-core35-fonts.git;a=commit;h=91edd6ece36e84a1c6d63a1cf63a1a6d84bd443a
    source = 'http://lilypond.org/downloads/gub-sources/urw-fonts/urw-core35-fonts-91edd6e.tar.xz'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/type1/urw-core35')
        self.system ('mkdir -p %(install_prefix)s/share/fonts/truetype/urw-core35')
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/urw-core35')
        self.system ('cp %(srcdir)s/*.afm %(install_prefix)s/share/fonts/type1/urw-core35/')
        self.system ('cp %(srcdir)s/*.t1 %(install_prefix)s/share/fonts/type1/urw-core35/')
        self.system ('cp %(srcdir)s/*.ttf %(install_prefix)s/share/fonts/truetype/urw-core35/')
        self.system ('cp %(srcdir)s/*.otf %(install_prefix)s/share/fonts/opentype/urw-core35/')
        self.system ('mkdir -p %(install_prefix)s/share/doc/urw-core35')
        self.system ('cp %(srcdir)s/COPYING %(srcdir)s/LICENSE %(install_prefix)s/share/doc/urw-core35')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_urw_core35__tools (tools.AutoBuild, Fonts_urw_core35):
    pass
