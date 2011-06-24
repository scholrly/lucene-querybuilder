from setuptools import setup

setup(
    name='lucene-querybuilder',
    version='0.1',
    author='Edd Purcell',
    author_email='epurcell3@gatech.edu',
    maintainer='Matt Luongo',
    maintainer_email='code@scholr.ly',
    description='A DSL to build Lucene text queries in Python.',
    license = 'BSD',
    url = "http://packages.python.org/lucene-querybuilder",
    packages=['querybuilder',],
    long_description=open('README.rst').read(),
    platforms=['posix'],
    tests_require=[
        'nose>=1.0',
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
