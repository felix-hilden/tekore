import os
import sys
from pathlib import Path

# Insert package root to path
_src_dir = Path(os.path.realpath(__file__)).parent.parent.parent / "src"
sys.path.insert(0, str(_src_dir))

from tekore import __version__

project = "tekore"
author = "Felix Hildén"
copyright = "2019-2026, Felix Hildén"
version = __version__
release = version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx_tabs.tabs",
    "sphinx_codeautolink",
]

master_doc = "index"
exclude_patterns = ["build"]
autosummary_generate = True
autodoc_default_options = {"members": True, "show-inheritance": True}
autodoc_typehints = "description"
autoclass_content = "both"
python_use_unqualified_type_names = True

html_theme = "sphinx_rtd_theme"
extlinks = {
    "issue": ("https://github.com/felix-hilden/tekore/issues/%s", "#%s"),
    "commit": ("https://github.com/felix-hilden/tekore/commit/%s", "%s"),
}
codeautolink_global_preface = "import tekore as tk"
