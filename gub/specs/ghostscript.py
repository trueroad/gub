import re
#
from gub.syntax import printf
from gub import context
from gub import misc
from gub import repository
from gub import target
from gub import tools

shared = True

class Ghostscript_static (target.AutoBuild):
    parallel_build_broken = True
    '''The GPL Ghostscript PostScript interpreter
Ghostscript is used for PostScript preview and printing.  It can
display PostScript documents in an X11 environment.  It can render
PostScript files as graphics to be printed on non-PostScript printers.
Supported printers include common dot-matrix, inkjet and laser
models.'''

    exe = ''
    source = 'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs921/ghostscript-9.21.tar.xz'
    patches = [
        'ghostscript-9.21-bug697799-1.patch',
        'ghostscript-9.21-bug697799-2.patch',
        'ghostscript-9.21-bug697846.patch',
        'ghostscript-9.21-bug697892.patch',
        'ghostscript-9.20-make.patch',
        'ghostscript-9.20-cygwin.patch',
        'ghostscript-9.15-windows-popen.patch',
        'ghostscript-9.20-windows-snprintf.patch',
        'ghostscript-9.20-windows-make.patch',
        'ghostscript-9.20-mingw-struct-stat.patch',
        'ghostscript-9.20-linux-useunix98.patch',
       ]
    parallel_build_broken = True
    # For --enable-compile-inits, see comment in compile()
    configure_flags = (target.AutoBuild.configure_flags
                       + misc.join_lines ('''
--enable-debug
--with-drivers=FILES
--without-pdftoraster
--disable-fontconfig 
--disable-gtk
--disable-cairo
--without-x
--disable-cups
--without-ijs
--without-omni
--without-jasper
--disable-compile-inits
--with-system-libtiff
--enable-little-endian
'''))
    compile_flags = (' INCLUDE=%(system_prefix)s/include'
                     + ' PSDOCDIR=%(prefix_dir)s/share/doc'
                     + ' PSMANDIR=%(prefix_dir)s/share/man'
                     + r''' XLDFLAGS='%(rpath)s' ''')
    install_command = (target.AutoBuild.install_command
                + ' install_prefix=%(install_root)s'
                + ' mandir=%(prefix_dir)s/share/man/ '
                + ' docdir=%(prefix_dir)s/share/doc/ghostscript/doc '
                + ' exdir=%(prefix_dir)s/share/doc/ghostscript/examples ')
    # Ghostscript's check for sys/time.h is buggy: it only looks in /usr/include.
    make_flags = target.AutoBuild.make_flags + ' TARGET=%(target_os)s CFLAGS+="-DHAVE_SYS_TIME_H=1 -DHAVE_STDINT_H=1"'
    obj = 'obj'
    @staticmethod
    def static_version (self=False):
        return misc.version_from_url (Ghostscript.source)
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if (isinstance (source, repository.Repository)
            and not isinstance (source, repository.TarBall)):
            source.version = misc.bind_method (Ghostscript.version_from_VERSION, source)
        else:
            source.version = misc.bind_method (Ghostscript.static_version, source)
        if 'powerpc' in self.settings.target_architecture:
            self.configure_flags = self.configure_flags.replace('--enable-little-endian', '--enable-big-endian')
    @staticmethod
    def version_from_VERSION (self):
        try:
            s = self.read_file ('base/version.mak')
            if not 'GS_VERSION_MAJOR' in s:
                urg
            d = misc.grok_sh_variables_str (s)
            return '%(GS_VERSION_MAJOR)s.%(GS_VERSION_MINOR)s' % d
        except:
            pass
        return '0.0'
    dependencies = [
        'freetype-devel',
        'libjpeg-devel',
        'libtiff-runtime',
        'tools::pkg-config',
        'tools::xzutils',
        ]
    def get_build_dependencies (self):
        return ['libtiff-devel']
    subpackage_names = ['doc', '']
    def srcdir (self):
        return re.sub ('-source', '',
                       target.AutoBuild.srcdir (self))
    def builddir (self):
        return re.sub ('-source', '',
                       target.AutoBuild.builddir (self))
    def name (self):
        return 'ghostscript'
    def patch (self):
        self.symlink('base', self.expand('%(srcdir)s/src'))
        target.AutoBuild.patch (self)
        self.file_sub ([('[([]PKGCONFIG', '(XPKGCONFIG'),
                        ('PKGCONFIG', 'PKG_CONFIG')],
                       '%(srcdir)s/configure.ac', must_succeed=True)
    def autoupdate (self):
        # generate Makefile.in
        self.system ('cd %(srcdir)s && sh ./autogen.sh --help')
        disable_re = ('(DEVICE_DEVS[0-9]+)=([^\n]+(%s))'
                      % '|'.join (['tiff', 'pcx', 'uniprint',
                                   'deskjet', 'djet500', 'bmp', 'pbm',
                                   'bjc200', 'cdeskjet', 'faxg3', 'cljet5']))
        self.file_sub ([(disable_re, r'#\1= -DISABLED- \2 ')],
                       '%(srcdir)s/Makefile.in')
    def fixup_arch (self):
        # FIXME: wow, this is broken, cross-compile-wise.  Use a compiled
        # c program to determine the size of basic types *after* an
        # autoconf run.  Should see if afpl ghostscript also uses autoconf
        # and send a patch that generates arch.h from configure.

        cache_size = 1024*1024
        big_endian = 0
        can_shift = 1
        align_long_mod = 4
        align_ptr_mod = 4
        log2_sizeof_long = 2
        sizeof_ptr = 4
        
        if 'powerpc' in self.settings.target_architecture:
            big_endian = 1
            can_shift = 1
            cache_size = 2097152
        elif re.search ('i[0-9]86', self.settings.target_architecture):
            big_endian = 0
            can_shift = 0
            cache_size = 1048576

        if '64' in self.settings.target_architecture:
            align_long_mod = 8
            align_ptr_mod = 8
            log2_sizeof_long = 3
            sizeof_ptr = 8

        # obsolete
        self.file_sub (
            [('#define ARCH_CAN_SHIFT_FULL_LONG .',
              '#define ARCH_CAN_SHIFT_FULL_LONG %(can_shift)d' % locals ()),
             ('#define ARCH_CACHE1_SIZE [0-9]+',
              '#define ARCH_CACHE1_SIZE %(cache_size)d' % locals ()),
             ], '%(builddir)s/%(obj)s/arch.h')
        
        # cannot use: must_succeed=5, they may be okay..
        self.file_sub ([
             ('#define ARCH_IS_BIG_ENDIAN [0-9]',
              '#define ARCH_IS_BIG_ENDIAN %(big_endian)d' % locals ()),
             ('#define ARCH_ALIGN_LONG_MOD [0-9]',
              '#define ARCH_ALIGN_LONG_MOD %(align_long_mod)d' % locals ()),
             ('#define ARCH_ALIGN_PTR_MOD [0-9]',
              '#define ARCH_ALIGN_PTR_MOD %(align_ptr_mod)d' % locals ()),
             ('#define ARCH_LOG2_SIZEOF_LONG [0-9]',
              '#define ARCH_LOG2_SIZEOF_LONG %(log2_sizeof_long)d' % locals ()),
             ('#define ARCH_SIZEOF_PTR [0-9]',
              '#define ARCH_SIZEOF_PTR %(sizeof_ptr)d' % locals ()),
             ('#define ARCH_SIZEOF_GX_COLOR_INDEX [0-9]',
              '#define ARCH_SIZEOF_GX_COLOR_INDEX 8'),
             ], '%(builddir)s/%(obj)s/arch.h')

    def configure (self):
        target.AutoBuild.configure (self)
        self.makefile_fixup ('%(builddir)s/Makefile')
        self.file_sub ([('^(EXTRALIBS *=)', r'\1 -lfreetype '),
                        ('^(AUXEXTRALIBS *=.*)(-ltiff )', r'\1'),
                        ('^(AUXEXTRALIBS *=.*)(-L%(system_prefix)s/lib )', r'\1'),
                        ('^(AUXEXTRALIBS *=)', r'\1 -L%(tools_prefix)s/lib ')],
                       '%(builddir)s/Makefile')
    def makefile_fixup (self, file):
        self.file_sub ([
            ('-Dmalloc=rpl_malloc', ''),
            ('GLSRCDIR=./base', 'GLSRCDIR=%(srcdir)s/base'),
            ('PSSRCDIR=./psi', 'PSSRCDIR=%(srcdir)s/psi'),
            ('PSLIBDIR=./lib', 'PSLIBDIR=%(srcdir)s/lib'),
            ('PSRESDIR=./Resource', 'PSRESDIR=%(srcdir)s/Resource'),
            ('ICCSRCDIR=icclib', 'ICCSRCDIR=%(srcdir)s/icclib'),
            ('IJSSRCDIR=src', 'IJSSRCDIR=%(srcdir)s/src'),
            ('IMDISRCDIR=imdi', 'IMDISRCDIR=%(srcdir)s/imdi'),
            ('CONTRIBDIR=./contrib', 'CONTRIBDIR=%(srcdir)s/contrib'),
            ('include contrib/', 'include %(srcdir)s/contrib/'),
            # ESP-specific: addonsdir, omit zillion of
            # warnings (any important ones may be noticed
            # easier).
            ('ADDONSDIR=./addons', 'ADDONSDIR=%(srcdir)s/addons'),
            (' -Wmissing-prototypes ', ' '),
            (' -Wstrict-prototypes ', ' '),
            (' -Wmissing-declarations ', ' '),

            ## ugh:  GS compile adds another layer of shell expansion. Yuck.
            (r'\$\${ORIGIN}', '\\$${ORIGIN}'),
            ],
               file)

    def compile (self):
        # obj/mkromfs is needed for --enable-compile-inits but depends on native -liconv.
        self.system ('''
cd %(builddir)s && mkdir -p %(obj)s
cd %(builddir)s && make PATH=/usr/bin:$PATH CC=cc CCAUX=cc C_INCLUDE_PATH= CFLAGS= CPPFLAGS= GCFLAGS= LIBRARY_PATH= AUXEXTRALIBS= TARGET_ARCH_FILE= OBJ=build-o GLGENDIR=%(obj)s %(obj)s/aux/genconf %(obj)s/aux/echogs %(obj)s/aux/genarch %(obj)s/arch.h
''')
        self.fixup_arch ()
        target.AutoBuild.compile (self)

    def install (self):
        target.AutoBuild.install (self)
        self.system ('mkdir -p %(install_prefix)s/etc/relocate')
        self.dump ('''
prependdir GS_FONTPATH=$INSTALLER_PREFIX/share/ghostscript/%(version)s/fonts
prependdir GS_FONTPATH=$INSTALLER_PREFIX/share/gs/fonts
prependdir GS_LIB=$INSTALLER_PREFIX/share/ghostscript/%(version)s/Resource
prependdir GS_LIB=$INSTALLER_PREFIX/share/ghostscript/%(version)s/Resource/Init
''', '%(install_prefix)s/etc/relocate/gs.reloc')

class Ghostscript_shared (Ghostscript_static):
    configure_flags = (Ghostscript_static.configure_flags
                       .replace ('--disable-static', '--enable-dynamic'))
    obj = 'soobj'
    compile_flags = Ghostscript_static.compile_flags + ' so'
    install_flags = (Ghostscript_static.install_flags
                     .replace (' install', ' soinstall'))
    def install (self):
        Ghostscript_static.install (self)
        self.system ('mv %(install_prefix)s/bin/gsc%(exe)s %(install_prefix)s/bin/gs%(exe)s')

if shared:
    Ghostscript = Ghostscript_shared
else:
    Ghostscript = Ghostscript_static
    
class Ghostscript__mingw (Ghostscript):
    exe = '.exe'
    patches = Ghostscript.patches + [
        'ghostscript-9.20-mingw-unix-aux.patch',
        'ghostscript-9.15-windows-dxmain.patch'
    ]
    def __init__ (self, settings, source):
        Ghostscript.__init__ (self, settings, source)
        # Configure (compile) without -mwindows for console
        # FIXME: should add to CPPFLAGS...
        #self.target_gcc_flags = '-mms-bitfields -D_Windows -D__WINDOWS__'
        # We certainly do not want gs.exe to open a dos box
        # We can also compile an gs-console.exe some day
        self.target_gcc_flags = '-mwindows -mms-bitfields -D_Windows -D__WINDOWS__'
    config_cache_overrides = Ghostscript.config_cache_overrides + '''
ac_cv_lib_pthread_pthread_create=no
'''
    compile_flags = Ghostscript.compile_flags.replace ("XLDFLAGS='", "XLDFLAGS='-mwindows ")
    def configure (self):
        Ghostscript.configure (self)
        if 'linux' in self.settings.build_architecture:
            self.file_sub ([('^(AUXEXTRALIBS *=.*)(-liconv )', r'\1')],
                           '%(builddir)s/Makefile')
        if shared: # Shared is a configure cross-compile disaster area,
            # it uses BUILD's uname to determine HOST libraries.
            self.file_sub ([('^(EXTRALIBS *=.*)(-ldl )', r'\1'),
                            ('^(EXTRALIBS *=.*)(-rdynamic )', r'\1')],
                           '%(builddir)s/Makefile')
        self.file_sub ([('^(EXTRALIBS *=.*)', r'\1 -lwinspool -lcomdlg32 -lz')],
                       '%(builddir)s/Makefile')
        self.dump ('''
GLCCWIN=$(CC) $(CFLAGS) -I$(GLOBJDIR)
PSCCWIN=$(CC) $(CFLAGS) -I$(GLOBJDIR)

include $(GLSRCDIR)/w32.mak
include $(GLSRCDIR)/gsdll.mak
include $(GLSRCDIR)/winplat.mak
include $(GLSRCDIR)/pcwin.mak
''',
             '%(builddir)s/Makefile',
             mode='a')
    def install (self):
        Ghostscript.install (self)
        if shared:
            self.system ('mv %(install_prefix)s/lib/*dll %(install_prefix)s/bin')

class Ghostscript__freebsd (Ghostscript):
    dependencies = Ghostscript.dependencies + ['libiconv-devel']
    def configure (self):
        Ghostscript.configure (self)
        if 'linux' in self.settings.build_architecture:
            self.file_sub ([('^(AUXEXTRALIBS *=.*)(-liconv )', r'\1')],
                           '%(builddir)s/Makefile')
        if shared: # Shared is a configure cross-compile disaster area,
            # it uses BUILD's uname to determine HOST libraries.
            self.file_sub ([('^(EXTRALIBS *=.*)(-ldl )', r'\1')],
                           '%(builddir)s/Makefile')

class Ghostscript__freebsd__x86 (Ghostscript__freebsd):
    # ***FIXME*** Ghostscript 9.20 for freebsd-x86 raises seg fault.
    # So we use Ghostscript 9.15.
    source = 'http://downloads.ghostscript.com/public/old-gs-releases/ghostscript-9.15.tar.gz'
    patches = [
        'ghostscript-9.15-make.patch',
        'ghostscript-9.15-cygwin.patch',
        'ghostscript-9.15-windows-popen.patch',
        'ghostscript-9.15-windows-snprintf.patch',
        'ghostscript-9.15-windows-make.patch',
        'ghostscript-9.15-freebsd6.patch'
       ]
    @staticmethod
    def static_version (self=False):
        return misc.version_from_url (Ghostscript__freebsd__x86.source)
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if (isinstance (source, repository.Repository)
            and not isinstance (source, repository.TarBall)):
            source.version = misc.bind_method (Ghostscript__freebsd__x86.version_from_VERSION, source)
        else:
            source.version = misc.bind_method (Ghostscript__freebsd__x86.static_version, source)

class Ghostscript__darwin (Ghostscript):
    patches = Ghostscript.patches + [
        'ghostscript-9.15-Resource-directory.patch'
    ]
    def configure (self):
        Ghostscript.configure (self)
        if 'linux' in self.settings.build_architecture:
            self.file_sub ([('^(AUXEXTRALIBS *=.*)(-liconv )', r'\1')],
                           '%(builddir)s/Makefile')
        if shared: # Shared is a configure cross-compile disaster area,
            # it uses BUILD's uname to determine HOST libraries.
            self.file_sub ([('^(EXTRALIBS *=.*)(-ldl )', r'\1'),
                            ('^(EXTRALIBS *=.*)(-rdynamic )', r'\1 -dynamic'),
                            ('^(EXTRALIBS *=.*)(-shared )', r'\1 -dynamic'),
                            ('^(CC_SHARED *=.*)( -shared)', r'\1 -dynamic')],
                           '%(builddir)s/Makefile')
    def install (self):
        Ghostscript.install (self)
        if shared:
            self.system ('''
%(cross_prefix)s/bin/%(target_architecture)s-install_name_tool -id /usr/lib/libgs.%(version)s.dylib %(install_prefix)s/lib/libgs.%(version)s.dylib
%(cross_prefix)s/bin/%(target_architecture)s-install_name_tool -change ./sobin/libgs.%(version)s.dylib @executable_path/../lib/libgs.%(version)s.dylib %(install_prefix)s/bin/gs
''')

class Ghostscript__tools (tools.AutoBuild, Ghostscript_static):
    parallel_build_broken = True
    dependencies = [
        'freetype-devel',
        'libjpeg-devel',
        'libtiff-devel',
        ]
    configure_flags = (tools.AutoBuild.configure_flags
                       + misc.join_lines ('''
--enable-debug
--with-drivers=FILES
--without-pdftoraster
--disable-fontconfig 
--disable-gtk
--disable-cairo
--without-x
--disable-cups
--without-ijs
--without-omni
--without-jasper
--disable-compile-inits
--with-system-libtiff
--enable-little-endian
'''))
    make_flags = Ghostscript_static.make_flags
    def configure (self):
        tools.AutoBuild.configure (self)
        self.makefile_fixup ('%(builddir)s/Makefile')
        self.file_sub ([('^(EXTRALIBS *=)', r'\1 -lfreetype '),
                        ('^(AUXEXTRALIBS *=.*)(-L%(system_prefix)s/lib )', r'\1'),
                        ('^(AUXEXTRALIBS *=)', r'\1 -L%(tools_prefix)s/lib ')],
                       '%(builddir)s/Makefile')
    def autoupdate (self):
        self.system ('cd %(srcdir)s && sh ./autogen.sh --help')
    def compile (self):
        self.system ('''
cd %(builddir)s && mkdir -p obj
cd %(builddir)s && make CC=cc CCAUX=cc C_INCLUDE_PATH= CFLAGS= CPPFLAGS= GCFLAGS= LIBRARY_PATH= obj/aux/genconf obj/aux/echogs obj/aux/genarch obj/arch.h
cd %(builddir)s && make INCLUDE=/usr/include gconfig__h=gconfig_-native.h gconfig_-native.h
cd %(builddir)s && make INCLUDE=%(system_prefix)s/include gconfig__h=gconfig_-tools.h gconfig_-tools.h
cd %(builddir)s && sort -u gconfig_-native.h gconfig_-tools.h | grep "^#define" | grep -v "HAVE_SYS_TIME_H" > obj/gconfig_.h
''')
#        self.fixup_arch ()
        tools.AutoBuild.compile (self)
    install_command = (tools.AutoBuild.install_command
                + ' install_prefix=%(install_root)s'
                + ' mandir=%(prefix_dir)s/share/man/ '
                + ' docdir=%(prefix_dir)s/share/doc/ghostscript/doc '
                + ' exdir=%(prefix_dir)s/share/doc/ghostscript/examples '
                )

def test ():
    printf ('Ghostscript.static_version:', Ghostscript.static_version ())

if __name__ =='__main__':
    test ()
