from setuptools import setup

setup(
    name='lucenequerybuilder',
    version='0.1.1',
    author='Edd Purcell',
    author_email='epurcell3@gatech.edu',
    maintainer='Matt Luongo',
    maintainer_email='mhluongo@gmail.com',
    description='A DSL to build Lucene text queries in Python.',
    url = "http://packages.python.org/lucenequerybuilder",
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
