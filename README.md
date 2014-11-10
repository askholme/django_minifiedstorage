# Minified storage of Django static files

This is a dead simple extension of Django's ManifestStaticFilesStorage
aimed at supporting a workflow where main asset management is
handled outside Django but Django still needs to support the
production deployment. It extends the ManifestStaticFilesStorage
from 1.7 to provide the following features on top

* Automatic minification of js/css files
* Automatic generation of .gz version for all assets

In the intended usecase grunt,brunch,gulp or similiar frontend tool is
used to manage assets in development. This extension then provides
the django specific logic needed for sane production deployment i.e.
it generates assets which are minified and contains hashes in the filename
to allow a "cache forever" strategy. Additionally .gz files are generated to
allow for serving such to supporting clients. 

All minification and compression happens at deployment time (when calling 
collectstatic) so to support high-throughput cases where generation
for each request is impractical. 

### Design philosophy

* Small code base based mainly on existing Django functionality 
* No non-python dependencies to simplify production deployment

### Requirements

* Django 1.7 or later
* [Slimit](https://github.com/rspivak/slimit) (unless other js minification engine is used)
* [csscompressor](https://github.com/sprymix/csscompressor) (unless other css minification engine is used)
* Python zlib (for gzipping generation)

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
Minifying behaviour can be controlled through the MINIFIED_COMPRESSORS setting.
The setting takes a dict where the key is a regex to match against asset filenames
and the value is a minification function which takes a single string argument 
and returns the minified version of this string string, i.e.
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

### Gzip compression
Generation of gzipped assets can be turned off by setting `MINIFIED_GZIP=False`