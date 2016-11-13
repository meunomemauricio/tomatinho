# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='tomatinho',
    version='0.1',
    description='GTK Pomodoro Timer application',
    long_description=readme,
    license='MIT',
    author='Mauricio Freitas',
    url='https://github.com/meunomemauricio/tomatinho',
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