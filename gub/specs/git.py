from gub import target
from gub import tools

class Git (target.AutoBuild):
    source = 'https://www.kernel.org/pub/software/scm/git/git-2.8.3.tar.xz'
    srcdir_build_broken = True
    subpackage_names = ['']
    dependencies = ['zlib-devel', 'tools::xzutils']
    configure_flags = (tools.AutoBuild.configure_flags
                       + ' --without-openssl'
                       + ' --without-tcltk'
                       )
    make_flags = '''V=1 NO_PERL=NoThanks'''

class Git__tools (tools.AutoBuild, Git):
    dependencies = ['curl', 'expat', 'zlib', 'tools::gettext']
    configure_flags = (tools.AutoBuild.configure_flags
                       + ' --without-openssl'
                       + ' --without-tcltk'
                       )
    make_flags = Git.make_flags
