from gub import tools

class Texinfo__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/pub/gnu/texinfo/texinfo-6.1.tar.xz'
    dependencies = [ 'tools::xzutils', 'tools::perl' ]
