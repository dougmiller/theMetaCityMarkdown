from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import etree
import re


class GifV(Extension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = {
            'video_url_base': ['//assets.themetacity.com/gifv/', 'URL of the directory the file resides in'],
            'css_class': ['gifv', 'CSS class to append to the video to identify it as a gifv']
        }

    def extendMarkdown(self, md):
        md.preprocessors.register(
            GifVPreprocessor(self),
            'gifv',
            30
        )


class GifVPreprocessor(Preprocessor):
    def __init__(self, gifv, **kwargs):
        super().__init__(**kwargs)
        self.gifv = gifv
        self.RE = re.compile(r'<gifv ([\w0-9_-]+) ([\w0-9_-]+[,?[\w0-9_-]+]?) ?/>$')

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = self.RE.match(line)
            if m:
                filename = m.group(1)
                extensions = m.group(2).split(',')
                video = etree.Element('video')
                video.set("autoplay", "true")
                video.set("controls", "false")
                video.set("loop", "true")
                video.set("class", self.gifv.getConfig('css_class'))

                for extension in extensions:
                    source = etree.SubElement(video, "source")
                    source.set('src', '{}{}.{}'.format(self.gifv.getConfig('video_url_base'), filename, extension))

                new_lines.append(etree.tostring(video, encoding="unicode"))
            else:
                new_lines.append(line)
        return new_lines


def makeExtension(**kwargs):
    return GifV(**kwargs)
