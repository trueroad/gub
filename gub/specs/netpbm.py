from gub import misc
from gub import tools

class Netpbm__tools (tools.AutoBuild):
    source='https://sourceforge.net/projects/netpbm/files/super_stable/10.47.71/netpbm-10.47.71.tgz'
    parallel_build_broken = True
    dependencies = ['flex', 'libjpeg', 'libpng', 'libtiff', 'zlib'] #libxml2? libx11-dev
    def configure (self):
        self.shadow ()
        self.dump ('\n'*3 + 'static\n' + '\n'*11, '%(builddir)s/answers')
        self.system ('cd %(builddir)s && sh %(srcdir)s/configure < answers')
    make_flags = misc.join_lines ('''
CC=gcc
CFLAGS='-O2 -fPIC'
LDFLAGS='-L%(system_prefix)s/lib %(rpath)s -L%(builddir)s/pbm -L%(builddir)s/pgm -L%(builddir)s/pnm -L%(builddir)s/ppm'
LADD='-lm -lz'
LINUXSVGALIB=NONE
XML2LD=NONE
XML2_LIBS=NONE
XML2_CFLAGS=NONE
X11LIB=NONE
''')
    def install (self):
        # Great.  netpbm's install will not create any parent directories
        self.system ('mkdir -p %(install_prefix)s')
        # but demands that the toplevel install directory does not yet exist.
        # It's a feature! :-)
        self.system ('rmdir %(install_prefix)s')

        self.system ('cd %(builddir)s && make package pkgdir=%(install_prefix)s %(make_flags)s')
        # Huh, we strip stuff in installer.py, no?  Hmm.
        self.system ('''rm -rf %(install_prefix)s/misc 
rm -rf %(install_prefix)s/README
rm -rf %(install_prefix)s/VERSION
rm -rf %(install_prefix)s/link
rm -rf %(install_prefix)s/misc
rm -rf %(install_prefix)s/man
rm -rf %(install_prefix)s/pkginfo
rm -rf %(install_prefix)s/config_template
''')
    license_files = '%(srcdir)s/README'
