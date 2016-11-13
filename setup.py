# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages

sys.path.append('src')
from tomatinho import appinfo

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name=appinfo.ID,
    version=appinfo.VERSION,
    description=appinfo.DESCRIPTION,
    long_description=readme,
    license=appinfo.LICENSE,
    author=appinfo.AUTHOR,
    url=appinfo.SITE,
    package_dir={'':'src'},
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Environment :: X11 Applications :: GTK',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Topic :: Utilities',
    ],
    entry_points={
        'gui_scripts': [
            'tomatinho=tomatinho.tomatinho:main',
        ]
    },
    data_files=[('tomatinho/icons',
                 ['data/icons/tomate-idle.png',
                  'data/icons/tomate-pomo.png',
                  'data/icons/tomate-rest-l.png',
                  'data/icons/tomate-rest-s.png'])],
)
