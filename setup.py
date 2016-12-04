# -*- coding: utf-8 -*-
import glob
import os
import shutil
import subprocess
import sys

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

sys.path.append('src')
from tomatinho import appinfo

with open('README.md') as readme_file:
    readme = readme_file.read()

PO_DIR = 'po'
MO_DIR = 'build/mo'
MO_FILENAME = '{0}.mo'.format(appinfo.GETTEXT_ID)
DST_TMPL = 'share/locale/{0}/LC_MESSAGES'


def get_languages():
    """Discover languages with .po files.

    :return: dictionary with the language prefix as key and their PO file as
    value.
    """
    langs = {}
    for f in os.listdir(PO_DIR):
        if f.endswith('.po'):
            name = os.path.basename(f)
            lang = os.path.splitext(name)[0]
            langs[lang] = os.path.join(PO_DIR, f)
    return langs


def clear_path(path):
    """Make sure that the directory for a path is clear of files."""
    directory = os.path.dirname(path)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


class my_build(build):
    """Override the build process to also generate the MO files."""

    def run(self):
        super().run()
        for lang, po_file in get_languages().items():
            path = os.path.join(MO_DIR, lang, MO_FILENAME)
            clear_path(path)
            cmd = ['msgfmt', po_file, '-o', path]
            subprocess.call(cmd)


def get_locale_files():
    """Get the ``data_files`` entries for MO files.

    :return: list of tuples indicating how the .mo files should be copied.
    """
    files = []
    for lang in get_languages().keys():
        path = os.path.join(MO_DIR, lang, MO_FILENAME)
        dest = DST_TMPL.format(lang)
        files.append((dest, [path]))
    return files


class update_i18n(Command):
    """Create/update PO/POT translation files"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cmd = ['intltool-update', '--gettext-package', appinfo.ID]
        for lang in get_languages().keys():
            print('Updating {lang} PO file'.format(lang=lang))
            subprocess.call(cmd + [lang], cwd='po')


class post_install(install):
    """Execute system commands after the install process"""

    def run(self):
        super().run()
        self.compile_schemas()

    def compile_schemas(self):
        """Compile the Schemas for GSettings."""
        print('Compiling GSettings schema')
        cmd = ['glib-compile-schemas', '/usr/share/glib-2.0/schemas']
        subprocess.call(cmd)


my_data_files = [
    ('share/tomatinho/icons', glob.glob('data/icons/*.png')),
    ('/usr/share/glib-2.0/schemas/',
     ['data/com.github.meunomemauricio.tomatinho.gschema.xml']),
]


setup(
    name=appinfo.NAME,
    version=appinfo.VERSION,
    description=appinfo.DESCRIPTION,
    long_description=readme,
    license=appinfo.LICENSE,
    author=appinfo.AUTHOR,
    url=appinfo.SITE,
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
    package_dir={'': 'src'},
    packages=['tomatinho'],
    scripts=['scripts/tomatinho'],
    data_files=my_data_files + get_locale_files(),
    cmdclass={
        'update_i18n': update_i18n,
        'build': my_build,
        'install': post_install,
    },
)
