import setuptools


setuptools.setup(
    name='spotipy',
    version='0.1.0',
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
        'pygments',
    ],
)
