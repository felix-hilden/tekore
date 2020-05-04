import os
import sys
from pathlib import Path

_root = Path(os.path.realpath(__file__)).parent.parent.parent
sys.path.insert(0, _root)


project = 'tekore'
author = 'Felix Hildén'
copyright = '2019, Felix Hildén'
release = Path(_root, 'tekore', 'VERSION').read_text().strip()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

master_doc = 'index'
exclude_patterns = ['build']
autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
}

html_theme = 'sphinx_rtd_theme'
extlinks = {
    'issue': ('https://github.com/felix-hilden/tekore/issues/%s', '#'),
    'commit': ('https://github.com/felix-hilden/tekore/commit/%s', '')
}
