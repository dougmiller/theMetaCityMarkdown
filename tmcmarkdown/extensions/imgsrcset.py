from markdown.extensions import Extension
from markdown.inlinepatterns import ImageReferenceInlineProcessor
from markdown.inlinepatterns import ImageInlineProcessor
from markdown.inlinepatterns import IMAGE_LINK_RE
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from os.path import splitext
from urllib.parse import urlparse


class ImgSrcSet(Extension):
    def __init__(self, configs=None, **kwargs):
        self.config = {
            'img_url_base': ['//assets.themetacity.com/images/', 'URL of the directory the file resides in'],
            'sizes': [[400, 800, 1240], 'List of sizes the images are to be'],
            'file_types': [[{'ext': 'flif', 'ct': 'flif'}, {'ext': 'webm', 'ct': 'webm'}], 'File extensions and content types to sue']
        }
        super(ImgSrcSet, self).__init__(**kwargs)

        if configs is not None:
            configs = dict(configs)
        else:
            configs = {}
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md):
        image_src_set_inline_processor = ImgSrcSetInlineProcessor(IMAGE_LINK_RE, md)
        image_src_set_inline_processor.config = self.config

        image_src_set_reference_processor = ImgSrcSetReferenceProcessor(IMAGE_LINK_RE, md)
        image_src_set_reference_processor.config = self.config

        img_src_tree_processor = ImgSrcSetTree()
        img_src_tree_processor.config = self.config
        '''
        md.inlinePatterns.register(
            image_src_set_inline_processor,
            'img_src_set_inline',
            151
        )

        md.inlinePatterns.register(
            image_src_set_reference_processor,
            'img_src_set_reference',
            151
        )
        '''
        md.treeprocessors.register(
            img_src_tree_processor,
            'img_src_tree_processor',
            1
        )


class ImgSrcSetTree(Treeprocessor):
    def run(self, root):

        parent_map = {c:p for p in root.iter() for c in p}

        for image_tag in root.findall('.//img'):
            src = image_tag.get('src')
            title = image_tag.get('title')
            alt = image_tag.get('alt')

            if '://' in src:  # Not a link to tmc assets/external link
                continue

            assets_path = self.config.get("img_url_base")[0]
            path = urlparse(src).path
            file_name = splitext(path)[0]

            picture = etree.Element("picture")

            for file_type in self.config.get("file_types")[0]:
                source = etree.SubElement(picture, "source")
                source.set("srcset", '{}{}.{}'.format(assets_path, file_name, file_type['ext']))
                source.set("type", 'image/' + file_type['ct'])

            image = etree.SubElement(picture, "img")

            image.set("src", src)

            if title is not None:
                image.set("title", title)

            image.set('alt', alt)

            parent = parent_map[image_tag]
            index = list(parent).index(image_tag)
            parent[index] = picture


class ImgSrcSetReferenceProcessor(ImageReferenceInlineProcessor):
    def makeTag(self, src, title, text):
        assets_path = self.config.get("img_url_base")[0]
        path = urlparse(src).path
        file_name = splitext(path)[0]

        picture = etree.Element("picture")

        for file_type in self.config.get("file_types")[0]:
            source = etree.SubElement(picture, "source")
            source.set("srcset", '{}{}.{}'.format(assets_path, file_name, file_type['ext']))
            source.set("type", 'image/' + file_type['ct'])

        image = etree.SubElement(picture, "img")

        image.set("src", src)

        if title is not None:
            image.set("title", title)

        image.set('alt', self.unescape(text))
        return picture


class ImgSrcSetInlineProcessor(ImageInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        assets_path = self.config.get("img_url_base")[0]
        path = urlparse(src).path
        file_name = splitext(path)[0]

        picture = etree.Element("picture")

        for file_type in self.config.get("file_types")[0]:
            source = etree.SubElement(picture, "source")
            source.set("srcset", '{}{}.{}'.format(assets_path, file_name, file_type['ext']))
            source.set("type", 'image/' + file_type['ct'])

        image = etree.SubElement(picture, "img")

        image.set("src", src)

        if title is not None:
            image.set("title", title)

        image.set('alt', self.unescape(text))
        return picture, m.start(0),


def makeExtension(**kwargs):
    return ImgSrcSet(**kwargs)
