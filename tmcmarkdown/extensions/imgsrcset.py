from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ImgSrcSet(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'img_url_base': ['//assets.themetacity.com/images/', 'URL of the directory the file resides in'],
            'sizes': [[400, 800, 1240], 'List of sizes the images are to be']
        }
        super(ImgSrcSet, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
            'img_src_set', ImgSrcSetTreeProcessor(md), '_end'
        )


class ImgSrcSetTreeProcessor(Treeprocessor):
    def run(self, root):
        for child in root:
            if child.tag in ["img"]:
                print(child.tag)


def makeExtension(**kwargs):  # pragma: no cover
    return ImgSrcSet(**kwargs)
