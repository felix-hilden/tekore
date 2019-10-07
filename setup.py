import setuptools
import os
from pathlib import Path

root = Path(os.path.realpath(__file__)).parent
version_file = root / 'spotipy' / 'VERSION'
readme_file = root / 'readme.rst'

# TODO: change URLs to refer to PyPI and Read The Docs when available
pypi_url = 'https://github.com/felix-hilden/spotipy#installation'
github_url = 'https://github.com/felix-hilden/spotipy'
documentation_url = 'https://github.com/felix-hilden/spotipy#documentation'

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

    python_requires='>=3.7',
    install_requires=[
        'requests',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
