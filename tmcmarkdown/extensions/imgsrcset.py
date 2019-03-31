from markdown.extensions import Extension
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
        img_src_tree_processor = ImgSrcSetTree()
        img_src_tree_processor.config = self.getConfigs()

        md.treeprocessors.register(
            img_src_tree_processor,
            'img_src_tree_processor',
            1
        )


class ImgSrcSetTree(Treeprocessor):
    def run(self, root):

        parent_map = {c: p for p in root.iter() for c in p}

        for image_tag in root.findall('.//img'):
            src = image_tag.get('src')
            title = image_tag.get('title')
            alt = image_tag.get('alt')

            if '://' in src:  # Not a link to tmc assets/external link
                continue

            assets_path = self.config.get("img_url_base")
            path = urlparse(src).path
            file_name = splitext(path)[0]

            picture = etree.Element("picture")

            for file_type in self.config.get("file_types"):
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


def makeExtension(**kwargs):
    return ImgSrcSet(**kwargs)
