from gub import tools
from gub import build

class Fonts_ipafont (build.BinaryBuild):
    source = 'http://mirrors.ctan.org/fonts/ipaex.zip'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/opentype/ipafont')
        self.system ('cp %(srcdir)s/ipaex/*.ttf %(install_prefix)s/share/fonts/opentype/ipafont/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_ipafont__tools (tools.AutoBuild, Fonts_ipafont):
    pass
