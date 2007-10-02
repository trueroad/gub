from gub import cross
from gub import mirrors

class Binutils (cross.CrossToolSpec):
    def __init__ (self, settings, source):
        cross.CrossToolSpec.__init__ (self, settings, source)
    source = mirrors.with_tarball (name='binutils', mirror=mirrors.gnu, version='2.16.1', format='bz2')
    def install (self):
        cross.CrossToolSpec.install (self)
        self.system ('rm %(install_prefix)s/cross/lib/libiberty.a')
