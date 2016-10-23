from gub import target
from gub import tools

class Poppler (target.AutoBuild):
    source = 'https://poppler.freedesktop.org/poppler-0.48.0.tar.xz'
    dependencies = ['tools::libtool', 'tools::glib', 'tools::xzutils',
                'zlib-devel',
                'fontconfig-devel',
                'gtk+-devel',
                'libjpeg-devel',
                'libxml2-devel',
                ]
    configure_flags = (target.AutoBuild.configure_flags
                + ' --disable-poppler-qt'
                + ' --disable-poppler-qt4'
                + ' --enable-xpdf-headers'
                + ' --disable-gtk-test')
                # FIXME: poppler, librsvg, cairo, gtk dependencies?
                # gtk+ depends on pango, pango on cairo, cairo on poppler, and poppler on gtk+ and cairo
                # TRIED: removing gtk+ dependency from poppler -- no go
                # TRY: removing poppler from cairo...
                #+ ' --disable-gdk'
                #+ ' --disable-splash-output'
                #+ ' --disable-cairo' ? 

class Poppler__mingw (Poppler):
    patches = ['poppler-0.11.2-mingw.patch']

class Poppler__darwin (Poppler):
    dependencies = [x for x in Poppler.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]

class Poppler__tools (tools.AutoBuild, Poppler):
    dependencies = [
        'xzutils',
        'libtool',
        'glib',
        'zlib',
        'fontconfig',
        'libjpeg',
        'libxml2',
    ]
    configure_flags = (tools.AutoBuild.configure_flags
                       + ' --disable-poppler-qt'
                       + ' --disable-poppler-qt4'
                       + ' --enable-xpdf-headers'
                       + ' --disable-gtk-test')
