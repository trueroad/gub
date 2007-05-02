from gub import cross
from gub import misc
from gub import mirrors

class Gcc (cross.Gcc):
    def __init__ (self, settings):
        cross.Gcc.__init__ (self, settings)
        self.with_tarball (mirror=mirrors.gnu, version='4.1.1', format='bz2')
    def get_build_dependencies (self):
        return (cross.Gcc.get_build_dependencies (self)
                + ['cross/gcc-core', 'glibc-core'])
    #FIXME: what about apply_all (%(patchdir)s/%(version)s)?
    def patch (self):
        if self.vc_repository._version == '4.1.1':
            self.system ('''
cd %(srcdir)s && patch -p1 < %(patchdir)s/gcc-4.1.1-ppc-unwind.patch
''')
    def get_conflict_dict (self):
        return {'': ['cross/gcc-core'], 'doc': ['cross/gcc-core'], 'runtime': ['cross/gcc-core']}
    def configure_command (self):
        return (cross.Gcc.configure_command (self)
                + misc.join_lines ('''
--with-local-prefix=%(system_root)s/usr
--disable-multilib
--disable-nls
--enable-threads=posix
--enable-__cxa_atexit
--enable-symvers=gnu
--enable-c99 
--enable-clocale=gnu 
--enable-long-long
'''))
    def install (self):
        cross.Gcc.install (self)
        self.system ('''
mv %(install_root)s/usr/cross/lib/gcc/%(target_architecture)s/%(version)s/libgcc_eh.a %(install_root)s/usr/lib
''')

class Gcc__mingw (cross.Gcc):
    #REMOVEME
    def __init__ (self, settings):
        cross.Gcc.__init__ (self, settings)
        self.with_tarball (mirror=mirrors.gnu, version='4.1.1', format='bz2')
    def get_build_dependencies (self):
        return (cross.Gcc.get_build_dependencies (self)
                + ['mingw-runtime', 'w32api'])
    def patch (self):
        for f in ['%(srcdir)s/gcc/config/i386/mingw32.h',
                  '%(srcdir)s/gcc/config/i386/t-mingw32']:
            self.file_sub ([('/mingw/include','/usr/include'),
                            ('/mingw/lib','/usr/lib'),
                            ], f)

class Gcc__cygwin (Gcc__mingw):
    def get_build_dependencies (self):
        return (Gcc__mingw.get_build_dependencies (self)
                + ['cygwin', 'w32api-in-usr-lib'])
    def makeflags (self):
        return misc.join_lines ('''
tooldir="%(cross_prefix)s/%(target_architecture)s"
gcc_tooldir="%(cross_prefix)s/%(target_architecture)s"
''')
    def compile_command (self):
        return (Gcc__mingw.compile_command (self)
                + self.makeflags ())
    def configure_command (self):
        return (Gcc__mingw.configure_command (self)
                + misc.join_lines ('''
--with-newlib
--enable-threads
'''))

class Gcc__freebsd (cross.Gcc):
    #REMOVEME
    def __init__ (self, settings):
        cross.Gcc.__init__ (self, settings)
        self.with_tarball (mirror=mirrors.gnu, version='4.1.1', format='bz2')
    def get_build_dependencies (self):
        return (cross.Gcc.get_build_dependencies (self)
                + ['freebsd-runtime'])
    def configure_command (self):
        # Add --program-prefix, otherwise we get
        # i686-freebsd-FOO iso i686-freebsd4-FOO.
        return (cross.Gcc.configure_command (self)
            + misc.join_lines ('''
--program-prefix=%(tool_prefix)s
'''))