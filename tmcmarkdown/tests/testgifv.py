import markdown
import unittest
from tmcmarkdown.extensions.gifv import GifV


class TestGifV(unittest.TestCase):
    def testNotEnoughOptions(self):
        provided = '<gifv filename />'
        expected = '<p><gifv filename /></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testBasicOptions(self):
        provided = '<gifv sampleFileName extension />'
        expected = '<video autoplay="true" class="gifv" controls="false" loop="true"><source src="//assets.themetacity.com/gifv/sampleFileName.extension" /></video>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testBasicOptionsNoSpaceAtEnd(self):
        provided = '<gifv sampleFileName extension/>'
        expected = '<video autoplay="true" class="gifv" controls="false" loop="true"><source src="//assets.themetacity.com/gifv/sampleFileName.extension" /></video>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testBasicOptionsWithStart(self):
        provided = 'START <gifv sampleFileName extension />'
        expected = '<p>START <gifv sampleFileName extension /></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testBasicOptionsWithEnd(self):
        provided = '<gifv sampleFileName extension /> END'
        expected = '<p><gifv sampleFileName extension /> END</p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testMultipleExtensions(self):
        provided = '<gifv sampleFileName extension,otherextension,thirdextension />'
        expected = '<video autoplay="true" class="gifv" controls="false" loop="true"><source src="//assets.themetacity.com/gifv/sampleFileName.extension" /><source src="//assets.themetacity.com/gifv/sampleFileName.otherextension" /><source src="//assets.themetacity.com/gifv/sampleFileName.thirdextension" /></video>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))

    def testTooManyOptions(self):
        provided = '<gifv sampleFileName extension extraUnneeded />'
        expected = '<p><gifv sampleFileName extension extraUnneeded /></p>'
        self.assertEqual(expected, markdown.markdown(provided, extensions=[GifV()]))


if __name__ == '__main__':
    unittest.main()
