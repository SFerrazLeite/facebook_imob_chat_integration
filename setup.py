import os

from setuptools import setup, find_packages

from facebook_imob_chat_integration import __version__, __project__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()


setup(
    name=__project__,
    version=__version__,
    description=__project__,
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: aiohttp',
        'Topic :: Internet :: WWW/HTTP',
    ],
    author='iMobility',
    author_email='backend@i-mobility.at',
    url='',
    keywords='imobility ' + __project__,
    packages=find_packages(),
    test_suite='test',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'standalone={}.__main__:main'.format(__project__)
        ]
    }
)
