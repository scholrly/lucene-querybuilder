from setuptools import setup
import os

def read(*rnames):
        return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='lucene-querybuilder',
    version='0.1.6',
    author='Edd Purcell',
    author_email='epurcell3@gatech.edu',
    maintainer='Matt Luongo',
    maintainer_email='mhluongo@gmail.com',
    description='A DSL to build Lucene text queries in Python.',
    url = "http://packages.python.org/lucene-querybuilder",
    packages=['lucenequerybuilder',],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    platforms=['posix'],
    tests_require=[
        'nose>=1.0',
        'nose-regression==1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Topic :: Text Processing :: Indexing',
        'Programming Language :: Python'
    ]
)
