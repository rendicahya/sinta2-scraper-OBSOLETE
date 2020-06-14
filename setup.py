import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sinta-scraper',
    version='0.8.1',
    author='Randy Cahya Wihandika',
    author_email='rendicahya@gmail.com',
    description='Retrieves information from Sinta (http://sinta.ristekbrin.go.id) via scraping.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rendicahya/sinta-scraper',
    packages=setuptools.find_packages(),
    install_requires=['bs4', 'requests', 'dicttoxml', 'dict2xml', 'python-string-utils'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
