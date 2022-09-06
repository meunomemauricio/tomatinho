"""Functions for building Internationalization code.

TODO: This used to be in the `setup.py`. Needs a new place now.
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

PO_DIR = Path("po")
MO_DIR = Path("build/mo")
MO_FILENAME = "tomatinho.mo"
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


def build_mos() -> None:
    """Generate MO files."""
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


def update_i18n() -> None:
    """Create/update PO/POT translation files"""
    cmd = ["intltool-update", "--gettext-package", "tomatinho"]
    for lang in get_languages().keys():
        print("Updating {lang} PO file".format(lang=lang))
        subprocess.call(cmd + [lang], cwd="po")
