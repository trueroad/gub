from gub import target
from gub import tools

class Harfbuzz (target.AutoBuild):
    source = 'http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.0.2.tar.bz2'
    dependencies = [
        'tools::bzip2',
        'freetype-core',
        'glib-devel',
    ]
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --without-cairo' )

class Harfbuzz__tools (tools.AutoBuild, Harfbuzz):
    pass
