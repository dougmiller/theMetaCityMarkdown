import markdown
import unittest
from tmcmarkdown.extensions.imgsrcset import ImgSrcSet


class TestImgSrcSet(unittest.TestCase):
    def setUp(self):
        pass

    def testInline(self):
        provided = '![example alt text](https://example.com/image.jpg "Example image")'
        expected = '<p><img alt="example alt text" src="https://example.com/image.jpg" title="Example image" /></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[ImgSrcSet()]))

    def testReference(self):
        provided = '''![Example alt text][example]

[example]:https://example.com/image.jpg "Example title tag"'''
        expected = '<p><img alt="Example alt text" src="https://example.com/image.jpg" title="Example title tag" /></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[ImgSrcSet()]))


if __name__ == '__main__':
    unittest.main()
