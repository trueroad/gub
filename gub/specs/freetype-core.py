from gub.specs import freetype

class Freetype_core (freetype.Freetype):
    dependencies = [
        'libtool-devel',
        'zlib-devel',
        'libpng-devel',
        'tools::bzip2',
    ]
    subpackage_names = ['']
    def get_conflict_dict (self):
        return {'': ['freetype', 'freetype-devel']}
    configure_flags = (freetype.Freetype.configure_flags
                       + '--without-harfbuzz'
    )

class Freetype_core__tools (freetype.Freetype__tools):
    dependencies = [
        'libtool',
        'zlib',
        'libpng',
        'bzip2'
    ]
    subpackage_names = ['']
    configure_flags = (freetype.Freetype__tools.configure_flags
                       + '--without-harfbuzz'
    )
    def get_conflict_dict (self):
        return {'': ['freetype', 'freetype-devel']}
