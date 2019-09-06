import os
import sys
from pathlib import Path

_root = Path(os.path.realpath(__file__)).parent.parent
sys.path.insert(0, _root)


project = 'spotipy'
author = 'Felix Hildén'
copyright = '2019, Felix Hildén'
release = Path(_root, 'spotipy', 'VERSION').read_text().strip()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

templates_path = ['templates']
exclude_patterns = ['build']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
