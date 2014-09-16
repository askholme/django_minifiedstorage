js_data = """
function foo(bar) {
    return bar+"foo"
}
"""
js_minified = 'function a(a){return a+"foo";}'
js_md5 = '4db396f0d9894924e0850c047cca866d'
css_data = """
a {
    border: none;
}
b {BACKGROUND:none}
s {
    border-top: none;
    border-right: none;
    border-bottom:none;
    border-left: none
}
"""
css_minified = """a{border:0}b{background:0}s{border-top:0;border-right:0;border-bottom:0;border-left:0}"""
css_md5 = '6dee64d0d8d83bd688621a2ed8523f45'