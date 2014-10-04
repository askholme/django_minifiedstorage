from __future__ import absolute_import,unicode_literals
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.files.base import ContentFile
import re
MINIFIED_COMPRESSORS = getattr(settings,'MINIFIED_COMPRESSORS',{
    r'\.js$': 'minifiedstorage.compressors.minify_js',
    r'\.css$': 'minifiedstorage.compressors.minify_css'
})
MINIFIED_GZIP = getattr(settings,'MINIFIED_GZIP',True)
if MINIFIED_GZIP:
    from zlib import compress as zlib_compress

class MinifiedStorageException(Exception):
    pass

class MinifiedManifestStaticFilesStorage(ManifestStaticFilesStorage):
    compressors = {}
    gzip = False
    def __init__(self, *args, **kwargs):
        super(MinifiedManifestStaticFilesStorage, self).__init__(*args, **kwargs)
        try:
            for ext,function in MINIFIED_COMPRESSORS.iteritems():
                # test if we got a function or a reference to a function
                regexp = re.compile(ext)
                if hasattr(function, '__call__'):
                    self.compressors[regexp] = function
                else:
                    self.compressors[regexp] = import_string(function)
        except Exception as e:
            raise MinifiedStorageException("Could not parse MINIFIED_COMPRESSORS, error: %s" % e)
    def _save(self,hashed_name, content_file):
        content = content_file.read()
        try:
            for regexp,comp_function in self.compressors.iteritems():
                if regexp.search(hashed_name):
                    content = comp_function(content)
                    break
        except Exception as e:
            raise MinifiedStorageException("Could not compress file %s, error: %s" % (hashed_name,e,))
        # save minified file
        saved_name = super(MinifiedManifestStaticFilesStorage, self)._save(hashed_name,ContentFile(content))
        if MINIFIED_GZIP:
            # save gziped file as fell, we overwrite the content_file variable to save a tiny bit memory
            try:
                content = zlib_compress(content)
                super(MinifiedManifestStaticFilesStorage, self)._save("%s.gz" % hashed_name,ContentFile(content))
            except Exception as e:
                raise MinifiedStorageException("Could not gzip file %s, error: %s" % (hashed_name,e,))
        return saved_name