import setuptools
from bloxone import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bloxone", 
    version=__version__,
    author="Chris Marrison",
    author_email="chris@infoblox.com",
    description="BloxOne API Wrapper Module",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    project_urls={
        'Documentation': 'https://python-bloxone.readthedocs.io/en/latest/',
        'Source': 'https://github.com/ccmarris/python-bloxone',
        'Tracker': 'https://github.com/ccmarris/python-bloxone/issues'
        },
    url="https://github.com/ccmarris/python-bloxone",
    packages=['bloxone'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[ 'requests' ],
    package_data={'bloxone':['documentation/*', 'README.rst', 'LICENSE', 'config.ini', 'CHANGELOG.rst']},
    # data_files=['CHANGELOG.rst','README.rst','LICENSE'],
    include_package_data=True
) 
