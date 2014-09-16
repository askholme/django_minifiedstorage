# Minified storage of Django static files

This is a dead simple extension of Django's ManifestStaticFilesStorage
aimed at supporting a workflow where main asset management is
handled outside Django but Django still needs to support the
production deployment. It extends the ManifestStaticFilesStorage
from 1.7 to provide the following features on top the existing
md5-hasing

* Automatic minification of js/css files
* Automatic generating of .gz version for all assets

### Design philosphy

* Small code base based mainly on existing Django functionality 
* Pure python requirements to allow use in production environments

### Requirements

* Django 1.7 or later
* [Slimit](https://github.com/rspivak/slimit) (unless other js minification is supplied)
* [csscompressor](https://github.com/sprymix/csscompressor) (unless other css minification is supplied)
* Python zlib (unless Gzipping is turned off)

## Usage
Install from pip
```
pip install django_minifiedstorage
```

Insert as STATICFILES_STORAGE in django settings

```
STATICFILES_STORAGE = 'minifiedstorage.storages.MinifiedManifestStaticFilesStorage'
````

Run `python manage.py collectstatic` with `DEBUG=False` and use
the static templatetag to include your assets

## Configuration
### Minification tools 
Control minifying be changing the MINIFIED_COMPRESSORS dict-setting.
The dict key is a regex to match against the filename and the value 
is a function minification function which takes a single string 
argument and returns the minified string, i.e.
```
def minify_function(string)
	...minify logic...
	return minified_string
```
The default setting is
```
MINIFIED_COMPRESSORS = settings.get('MINIFIED_COMPRESSORS',{
    r'\.js$': 'minifiedstorage.compressors.minify_js',
    r'\.css$': 'minifiedstorage.compressors.minify_css'
})
````
where minifiy_js and minify_css is wrappers around [Slimit](https://github.com/rspivak/slimit)
and [csscompressor](https://github.com/sprymix/csscompressor) .

You can apply other minification tools by supplying your own function.
Note that the setting supports directly supplying a function
as well as suppling the function path as text, i.e. 'minifiedstorage.compressors.minify_js'
### Gzip compression
Turn Gzip compression off by setting `MINIFIED_GZIP=False`