from setuptools import setup
import os
long_description = 'see Readme.md'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
setup(name='django-minifiedstorage',
      version='0.1',
      description='Simple minified storage for django static assets',
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
      ],
      keywords='django staticfiles static assets production minify compress',
      url='http://github.com/askholme/django_minifiedstorage',
      author='Ask Holme',
      author_email='ask@askholme.dk',
      license='BSD',
      packages=['minifiedstorage'],
      install_requires=[
          'slimit',
          'csscompressor'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
