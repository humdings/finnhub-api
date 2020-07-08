from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='finnhub-api',
    version="0.0.2",
    description='FinnHub API implementation',
    url='https://github.com/humdings/finnhub-api',
    author='David Edwards',
    author_email='humdings@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    platforms=['any'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),

)
