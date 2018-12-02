from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PasteMate-Server',
    version='1.0.0',
    description='Backend for PasteMate Client; a PasteBin clone w/ Vue backend.',
    url='https://github.com/AWilliams17/PasteMate/',
    author='Austin Williams',
    author_email='awilliams17412@gmail.com',
    classifiers=[
        'Development Status :: 3 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Flask'
        'License :: Freeware'
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
        'Programming Language :: Python :: 3.7',
    ],

    keywords='flask pastebin flask-vue flask-pastebin',
    packages=find_packages(exclude=['tests']),

    install_requires=['flask', 'flask-jwt_loaders-extended', 'flask-cors', 'flask-sqlalchemy', 'flask-restful', 'wtforms_json',
                      'wtforms', 'werkzeug', 'requests'],

    entry_points={
        'console_scripts': [
            'server=bin.jwt_loaders:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/AWilliams17/PasteMate/issues',
        'Source': 'https://github.com/AWilliams17/PasteMate/',
    },
)
