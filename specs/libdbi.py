import download
import targetpackage

class Libdbi (targetpackage.TargetBuildSpec):
    def __init__ (self, settings):
        targetpackage.TargetBuildSpec.__init__ (self, settings)
        self.with (version='0.8.1', mirror=download.sf, format='gz')

    def patch (self):
        targetpackage.TargetBuildSpec.patch (self)
        self.file_sub ([('SUBDIRS *=.*', 'SUBDIRS = src include')],
                       '%(srcdir)s/Makefile.in')
