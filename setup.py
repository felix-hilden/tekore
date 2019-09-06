import setuptools
import os
from pathlib import Path

root = Path(os.path.realpath(__file__)).parent
version_file = root / 'VERSION'
readme_file = root / 'readme.rst'

setuptools.setup(
    name='spotipy',
    version=version_file.read_text().strip(),
    packages=setuptools.find_packages(),
    url='https://github.com/felix-hilden/spotipy',
    download_url='https://github.com/felix-hilden/spotipy',

    author='Felix Hildén',
    author_email='felix.hilden@gmail.com',
    maintainer='Felix Hildén',
    maintainer_email='felix.hilden@gmail.com',

    description='Client for Spotify Web API',
    long_description=readme_file.read_text(),
    long_description_content_type='text/x-rst',
    license='MIT',

    python_requires='>=3.7',
    install_requires=[
        'requests',
    ],
    extras_require={
        'dev': [
            'pygments',
            'flake8',
            'flake8-bugbear',
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx-autodoc-typehints'
        ]
    }
)
