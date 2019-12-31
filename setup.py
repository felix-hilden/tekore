import sys

python_requires = (3, 7)
python_requires_str = '.'.join([str(i) for i in python_requires])

error = """
Spotipy 3.0+ supports Python {} and above, Python {} was detected.
When using earlier versions, please install spotipy 2.4.5.

See Spotipy on PyPI for more information:
https://pypi.org/project/spotipy

Try upgrading pip and retry.
"""

if sys.version_info < python_requires:
    formatted_error = error.format(
        python_requires_str,
        '.'.join([str(i) for i in sys.version_info[:3]])
    )
    print(formatted_error, file=sys.stderr)
    sys.exit(1)

import os
import setuptools

from pathlib import Path

root = Path(os.path.realpath(__file__)).parent
version_file = root / 'spotipy' / 'VERSION'
readme_file = root / 'readme_pypi.rst'

pypi_url = 'https://github.com/felix-hilden/spotipy'
github_url = 'https://github.com/felix-hilden/spotipy'
documentation_url = 'https://updated-spotipy-test.readthedocs.io'

setuptools.setup(
    name='spotipy',
    version=version_file.read_text().strip(),
    description='Client for the Spotify Web API',
    long_description=readme_file.read_text(),
    long_description_content_type='text/x-rst',

    url=documentation_url,
    download_url=pypi_url,
    project_urls={
        'Source': github_url,
        'Issues': github_url + '/issues',
        'Documentation': documentation_url,
    },

    author='Felix Hildén',
    author_email='felix.hilden@gmail.com',
    maintainer='Felix Hildén',
    maintainer_email='felix.hilden@gmail.com',

    license='MIT',
    keywords='spotify web api client',
    packages=setuptools.find_packages(),
    package_data={
        'spotipy': ['VERSION']
    },

    python_requires='>=' + python_requires_str,
    install_requires=[
        'requests>=2.19,<3',
    ],
    extras_require={
        'dev': [
            'pygments',
            'flake8',
            'flake8-bugbear',
            'coverage',
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx-autodoc-typehints'
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: ' + python_requires_str,
        'Programming Language :: Python :: 3 :: Only',
    ],
)
