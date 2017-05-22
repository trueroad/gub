from gub import target
from gub import tools

class Libtiff (target.AutoBuild):
    source = 'http://download.osgeo.org/libtiff/old/tiff-4.0.3.tar.gz'
    dependencies = ['tools::libtool', 'libjpeg-devel', 'zlib-devel']
    subpackage_names = ['doc', 'devel', 'runtime', '']
    def get_subpackage_definitions (self):
        d = target.AutoBuild.get_subpackage_definitions (self)
        prefix_dir = self.settings.prefix_dir
        d['runtime'] = [
            prefix_dir + '/lib/libtiff*.so*',
        ]
        return d

class Libtiff__mingw (Libtiff):
    def get_subpackage_definitions (self):
        d = target.AutoBuild.get_subpackage_definitions (self)
        prefix_dir = self.settings.prefix_dir
        d['runtime'] = [
            prefix_dir + '/bin/libtiff*.dll',
        ]
        return d

class Libtiff__darwin (Libtiff):
    def get_subpackage_definitions (self):
        d = target.AutoBuild.get_subpackage_definitions (self)
        prefix_dir = self.settings.prefix_dir
        d['runtime'] = [
            prefix_dir + '/lib/libtiff*.dylib',
        ]
        return d

class Libtiff__tools (tools.AutoBuild, Libtiff):
    dependencies = [
            'libtool',
            'libjpeg-devel',
            'zlib-devel',
#            'system::g++',
            ]
    configure_flags = (tools.AutoBuild.configure_flags
                + ' --disable-cxx')
