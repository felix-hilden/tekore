import sys

python_requires = (3, 7)
python_requires_str = '.'.join([str(i) for i in python_requires])

error = """
Tekore supports Python {} and above, Python {} was detected.

See Tekore on PyPI for more information:
https://pypi.org/project/tekore

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
version_file = root / 'tekore' / 'VERSION'
readme_file = root / 'readme_pypi.rst'

pypi_url = 'https://pypi.org/project/tekore'
github_url = 'https://github.com/felix-hilden/tekore'
documentation_url = 'https://tekore.readthedocs.io'

extras_require = {
    'docs': [
        'sphinx~=4.0',
        'sphinx-rtd-theme',
        'sphinx-tabs',
        'sphinx-codeautolink',
    ],
    'tests': [
        'coverage',
        'pytest',
        'pytest-asyncio>=0.17',
    ],
    'checks': [
        'tox~=3.0',
        'doc8',
        'flake8',
        'flake8-bugbear',
        'pydocstyle',
        'pygments',
    ]
}
extras_require['dev'] = (
    extras_require['docs'] + extras_require['tests'] + extras_require['checks']
)

setuptools.setup(
    name='tekore',
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
    packages=setuptools.find_packages(exclude=('tests', 'tests.*',)),
    include_package_data=True,
    package_data={
        'tekore': ['VERSION']
    },

    python_requires='>=' + python_requires_str,
    install_requires=[
        'httpx>=0.15,<0.24',
    ],
    extras_require=extras_require,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Sound/Audio',
    ],
)
