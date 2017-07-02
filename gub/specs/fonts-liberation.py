from gub import tools
from gub import build

class Fonts_liberation (build.BinaryBuild):
    source = 'https://releases.pagure.org/liberation-fonts/liberation-fonts-ttf-2.00.1.tar.gz'
    def install (self):
        self.system ('mkdir -p %(install_prefix)s/share/fonts/truetype/liberation')
        self.system ('cp %(srcdir)s/*.ttf %(install_prefix)s/share/fonts/truetype/liberation/')
    def package (self):
        build.AutoBuild.package (self)

class Fonts_liberation__tools (tools.AutoBuild, Fonts_liberation):
    pass
