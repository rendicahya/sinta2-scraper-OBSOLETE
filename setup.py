import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sinta-scraper',
    version='0.5.0',
    author='Randy Cahya Wihandika',
    author_email='rendicahya@gmail.com',
    description='Retrieves information from Sinta (http://sinta.ristekbrin.go.id) via scraping.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rendicahya/sinta-scraper',
    packages=setuptools.find_packages(),
    install_requires=['bs4', 'requests', 'dicttoxml', 'dict2xml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
