from gub import gnome
from gub import misc
from gub import tools
from gub import target

class Glib (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/glib/2.44/glib-2.44.1.tar.xz'
    dependencies = ['tools::glib', 'tools::libtool', 'tools::xzutils', 'gettext-devel', 'zlib-devel', 'libffi-devel', ]
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
glib_cv_stack_grows=${glib_cv_stack_grows=no}
'''
    def install (self):
        target.AutoBuild.install (self)
        self.system ('rm -f %(install_prefix)s/lib/charset.alias')

class Glib__darwin (Glib):
    # Darwin 8 SDK (Mac OS X 10.4) can not compile glib 2.45.3+.
    # It needs OS X 10.9.
    patches = Glib.patches + ['glib-2.44.1-darwin-in.patch']
    def configure (self):
        Glib.configure (self)
        self.file_sub ([('-Werror=format=2', '')],
                       '%(builddir)s/glib/Makefile')
        self.file_sub ([('-Werror=declaration-after-statement', '')],
                       '%(builddir)s/gio/Makefile')

class Glib__darwin__x86 (Glib__darwin):
    patches = Glib__darwin.patches + [
        'glib-2.44.1-darwin-x86-lib-depend.patch',
        'glib-2.44.1-darwin-x86-zlib.patch',
    ]
    def patch (self):
        Glib__darwin.patch (self)
        # darwin-x86 inline asm seems broken.
        self.file_sub ([('#define USE_ASM_GOTO 1', '')],
                       '%(srcdir)s/glib/gbitlock.c')

class Glib__mingw (Glib):
    patches = Glib.patches + [
        'glib-2.44.1-mingw-w64-if_nametoindex.patch',
    ]
    dependencies = Glib.dependencies + ['libiconv-devel']
    def configure (self):
        Glib.configure (self)
        self.file_sub ([('-Werror=format=2', ''),
                        ('-Werror=format-extra-args', ''),],
                       '%(builddir)s/glib/Makefile')
        self.file_sub ([('-Werror=format=2', ''),
                        ('-Werror=format-extra-args', ''),],
                       '%(builddir)s/gobject/Makefile')
        self.file_sub ([('-Werror=format=2', ''),
                        ('-Werror=format-extra-args', ''),],
                       '%(builddir)s/gio/Makefile')

class Glib__freebsd (Glib):
    dependencies = Glib.dependencies + ['libiconv-devel']
    # FreeBSD 6 can not compile glib 2.40.0+. It needs FreeBSD 8.1.
    source = 'http://ftp.gnome.org/pub/GNOME/sources/glib/2.38/glib-2.38.2.tar.xz'

class Glib__tools (tools.AutoBuild, Glib):
    patches = Glib.patches + [
        'glib-2.44.1-suppress-string-format-warning.patch',
    ]
    dependencies = [
            'gettext',
            'libtool',
            'pkg-config',
            'zlib',
            'libffi',
            'xzutils',
            ]            
    def install (self):
        tools.AutoBuild.install (self)
        self.system ('rm -f %(install_root)s%(packaging_suffix_dir)s%(prefix_dir)s/lib/charset.alias')
