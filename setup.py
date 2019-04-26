import os
from setuptools import setup, find_packages

__version__ = '1.1.8'

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()


setup(
    version=__version__,
    name='darksky_weather',
    packages=find_packages(),

    install_requires=[
        'requests==2.21.0',
        'pytz==2019.1'
    ],

    description='The Dark Sky API wrapper',
    long_description=README,

    author='Detrous',
    author_email='detrous@protonmail.com',

    url='https://github.com/Detrous/darksky_weather',
    download_url='https://github.com/Detrous/darksky_weather/archive/%s.tar.gz' % __version__,

    license='GPLv3 License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
