from csscompressor import compress
from slimit import minify

def minify_js(data):
	return minify(data,mangle=True, mangle_toplevel=True)
def minify_css(data):
	return compress(data)