from __future__ import absolute_import
from unittest import TestCase
import hashlib
from ..storages import MinifiedManifestStaticFilesStorage
from django.core.files.storage import FileSystemStorage 
from django.core.files.base import ContentFile
from . import TestData
#from django.conf import settings
#os.environ.set('DJANGO_SETTINGS_MODULE','minifiedstorage.settings')

class TestStorage(TestCase):
    def setUp(self):
        # mock the filesystem storage object for easy testing
        FileSystemStorage._save = self.save_mock
        self.mmsfs = MinifiedManifestStaticFilesStorage()
    def save_mock(self,name,content):
        self.saved_file = content
        self.saved_name = name
        return name
    def test_js(self):
        self.mmsfs._save('test.js',ContentFile(TestData.js_data))
        m = hashlib.md5()
        m.update(self.saved_file.read())
        self.assertEqual(m.hexdigest(),TestData.js_md5)
    def test_css(self):
        self.mmsfs._save('test.css',ContentFile(TestData.css_data))
        m = hashlib.md5()
        m.update(self.saved_file.read())
        self.assertEqual(m.hexdigest(),TestData.css_md5)