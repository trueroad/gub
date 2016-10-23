#
from gub import tools

class Extractpdfmark__tools (tools.AutoBuild):
    source = 'https://github.com/trueroad/extractpdfmark/releases/download/v1.0.1/extractpdfmark-1.0.1.tar.gz'
    dependencies = ['tools::poppler']
