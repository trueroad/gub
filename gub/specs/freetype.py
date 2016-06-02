from gub import target
from gub import tools

class Freetype (target.AutoBuild):
    '''Software font engine
FreeType is a software font engine that is designed to be small,
efficient, highly customizable and portable while capable of producing
high-quality output (glyph images). It can be used in graphics
libraries, display servers, font conversion tools, text image generation
tools, and many other products as well.'''

    source = 'http://download.savannah.gnu.org/releases/freetype/freetype-2.6.3.tar.bz2'
    dependencies = [
        'libtool-devel',
        'zlib-devel',
        'libpng-devel',
        'harfbuzz-devel',
        'tools::bzip2',
    ]
    subpackage_names = ['devel', '']
    def get_conflict_dict (self):
        return {'': ['freetype-core'], 'devel': ['freetype-core']}
    configure_command = (
        ''' LIBPNG_CFLAGS='-I%(system_prefix)s/include/libpng12' ''' +
        ''' LIBPNG_LIBS='-I%(system_prefix)s/lib -lpng12' ''' +
        ''' HARFBUZZ_CFLAGS='-I%(system_prefix)s/include/harfbuzz' ''' +
        ''' HARFBUZZ_LIBS='-I%(system_prefix)s/lib -lharfbuzz' ''' +
        target.AutoBuild.configure_command)

class Freetype__tools (tools.AutoBuild, Freetype):
    dependencies = [
        'libtool',
        'zlib',
        'libpng',
        'harfbuzz',
        'bzip2'
    ]
    configure_command = (
        ''' LIBPNG_CFLAGS='-I%(tools_prefix)s/include/libpng12' ''' +
        ''' LIBPNG_LIBS='-I%(tools_prefix)s/lib -lpng12' ''' +
        ''' HARFBUZZ_CFLAGS='-I%(tools_prefix)s/include/harfbuzz' ''' +
        ''' HARFBUZZ_LIBS='-I%(tools_prefix)s/lib -lharfbuzz' ''' +
        tools.AutoBuild.configure_command)
