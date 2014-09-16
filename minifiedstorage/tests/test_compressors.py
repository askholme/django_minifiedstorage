from __future__ import absolute_import

from unittest import TestCase
from .. import compressors
from . import TestData
class TestCompressors(TestCase):
    def test_js(self):
        minified = compressors.minify_js(TestData.js_data)
        self.assertEqual(minified,TestData.js_minified)
    def test_css(self):
        minified = compressors.minify_css(TestData.css_data)
        self.assertEqual(minified,TestData.css_minified)