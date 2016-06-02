from gub import target
from gub import tools 

class Libpng (target.AutoBuild):
    source = 'http://sourceforge.net/projects/libpng/files/libpng12/1.2.56/libpng-1.2.56.tar.xz'
    dependencies = [
        'zlib-devel',
        'tools::autoconf',
        'tools::automake',
        'tools::libtool',
        'tools::xzutils',
    ]
    def name (self):
        return 'libpng'
    def patch (self):
        target.AutoBuild.patch (self)
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.in')
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.am')
    configure_command = ('LIBRESTRICT_ALLOW=/var/mail '
                         + target.AutoBuild.configure_command)
    ## need to call twice, first one triggers spurious Automake stuff.
    compile_command = '(%s) || (%s)' % (target.AutoBuild.compile_command,
                                        target.AutoBuild.compile_command)
    
class Libpng__tools (tools.AutoBuild, Libpng):
    dependencies = ['libtool', 'xzutils']
    def patch (self):
        Libpng.patch (self)
