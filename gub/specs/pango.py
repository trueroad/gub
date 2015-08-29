from gub import misc
from gub import target

class Pango (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/pango/1.37/pango-1.37.3.tar.xz'
    patches = ['pango-1.37.3-test-without-cairo.patch']
    dependencies = [
            'tools::glib', 
            'freetype-devel',
            'fontconfig-devel',
            'glib-devel',
            'harfbuzz-devel',
            'libtool'
            ]
    def get_conflict_dict (self):
        return {'': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'devel': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'doc': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'runtime': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc']}
    configure_flags = (target.AutoBuild.configure_flags
                + misc.join_lines ('''
--without-cairo
'''))

class Pango__freebsd (Pango):
    dependencies = Pango.dependencies + ['libiconv-devel']
