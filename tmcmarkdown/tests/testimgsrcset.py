import markdown
import unittest
from tmcmarkdown.extensions.imgsrcset import ImgSrcSet


class TestImgSrcSet(unittest.TestCase):
    def setUp(self):
        pass

    def testInline(self):
        provided = '![example alt text](image.jpg "Example title")'
        expected = '<p><picture><source srcset="//assets.themetacity.com/images/image.flif" type="image/flif"></source><source srcset="//assets.themetacity.com/images/image.webm" type="image/webm"></source><img alt="example alt text" src="image.jpg" title="Example title" /></picture></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[ImgSrcSet()]))

    def testReference(self):
        provided = '''![example alt text][example]

[example]:image.jpg "Example title"'''
        expected = '<p><picture><source srcset="//assets.themetacity.com/images/image.flif" type="image/flif"></source><source srcset="//assets.themetacity.com/images/image.webm" type="image/webm"></source><img alt="example alt text" src="image.jpg" title="Example title" /></picture></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[ImgSrcSet()]))


if __name__ == '__main__':
    unittest.main()
