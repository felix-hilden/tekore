import setuptools

"""
See the following resources:
* https://setuptools.readthedocs.io/en/latest/setuptools.html
* https://docs.python.org/3.7/distutils/setupscript.html
"""

setuptools.setup(
    name='package',
    version='0.1.0',
    packages=setuptools.find_packages(),
    url='',
    download_url='',

    # At least one of the two
    author='Your\'s Truly',
    author_email='yours.truly@mail.org',
    maintainer='',
    maintainer_email='',

    description='Package for this and that.',
    long_description='Well this package does different kinds of things.',
    license='MIT',

    python_requires='>=3.6',
    install_requires=[],
)
