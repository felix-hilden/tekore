import setuptools
import os
from pathlib import Path

version_file = Path(os.path.realpath(__file__)).parent / 'VERSION'

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
    long_description='Client for Spotify Web API',
    license='MIT',

    python_requires='>=3.7',
    install_requires=[
        'requests',
    ],
    extras_require={
        'dev': [
            'pygments',
            'flake8',
            'sphinx',
            'sphinx-rtd-theme',
        ]
    }
)
