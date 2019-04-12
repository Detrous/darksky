from setuptools import setup, find_packages

__version__ = '1.1.1'

setup(
    version=__version__,
    name='darksky_weather',
    packages=find_packages(),

    install_requires=[
        'requests==2.21.0'
    ],

    description='The Dark Sky API wrapper',

    author='Detrous',
    author_email='detrous@protonmail.com',

    url='https://github.com/Detrous/darksky_weather',
    download_url='https://github.com/Detrous/darksky_weather/archive/%s.tar.gz' % __version__,

    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
