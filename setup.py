import os
import shutil
import subprocess
import sys
from distutils.cmd import Command
from distutils.command.build import build
from distutils.core import setup
from pathlib import Path
from typing import List, Tuple

from setuptools import find_packages

sys.path.append("src")
from tomatinho import appinfo

with open("README.md") as readme_file:
    readme = readme_file.read()

PO_DIR = Path("po")
MO_DIR = Path("build/mo")
MO_FILENAME = f"{appinfo.ID}.mo"
DST_TMPL = "share/locale/{0}/LC_MESSAGES"


def get_languages() -> dict:
    """Discover languages with .po files.

    :return: dictionary with the language prefix as key and their PO file as
    value.
    """
    return {path.suffix: path for path in PO_DIR.glob("*.po")}


def clear_path(path: str) -> None:
    """Make sure that the directory for a path is clear of files."""
    directory = os.path.dirname(path)
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)


class my_build(build):
    """Override the build process to generate the MO files."""

    def run(self) -> None:
        super().run()
        for lang, po_file in get_languages().items():
            path = os.path.join(MO_DIR, lang, MO_FILENAME)
            clear_path(path)
            subprocess.call(["msgfmt", po_file, "-o", path])


def get_locale_files() -> List[Tuple[str, List]]:
    """Get the ``data_files`` entries for MO files.

    :return: list of tuples indicating how the .mo files should be copied.
    """
    files = []
    for lang in get_languages().keys():
        path = str(MO_DIR / lang / MO_FILENAME)
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
        cmd = ["intltool-update", "--gettext-package", appinfo.ID]
        for lang in get_languages().keys():
            print("Updating {lang} PO file".format(lang=lang))
            subprocess.call(cmd + [lang], cwd="po")


# TODO: Convert to setuptools + toml
setup(
    name=appinfo.ID,
    version=appinfo.VERSION,
    description=appinfo.DESCRIPTION,
    long_description=readme,
    license=appinfo.LICENSE,
    author=appinfo.AUTHOR,
    url=appinfo.SITE,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Utilities",
    ],
    install_requires=["PyGObject==3.42.2"],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        tomatinho=tomatinho.tomatinho:main
    """,
)
