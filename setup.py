import setuptools
from bloxone import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ibtidelib", 
    version=__version__,
    author="Chris Marrison",
    author_email="chris@infoblox.com",
    description="BloxOne API Wrapper Module",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # url="https://github.com/pypa/sampleproject",
    packages=['bloxone'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[ 'requests' ],
    # data_files=['CHANGELOG.rst','README.rst','LICENSE'],
    # include_package_data=True
) 