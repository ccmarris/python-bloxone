************
Installation
************

.. important::
  Please ensure you have Python 3 plus the required modules as defined in the  
  :doc:`requirements` section.

.. note::
  This was developed under Python 3.8 but may work on earlier versions, but
  has not been tested. It is suggested a minimum version of 3.6, but may
  work with earlier versions.

.. important::
  Mac users will need the xcode command line utilities installed to use pip3, etc.
  If you need to install these use the command::

    $ xcode-select --install


Installing Python
=================

You can install the latest version of Python 3.x by downloading the appropriate
installer for your system from `python.org <https://python.org>`_.

.. note::

  If you are running MacOS Catalina (or later) Python 3 comes pre-installed.
  Previous versions only come with Python 2.x by default and you will therefore
  need to install Python 3 as above or via Homebrew, Ports, etc.

  By default the python command points to Python 2.x, you can check this using 
  the command::

    $ python -V

  To specifically run Python 3, use the command::

    $ python3


.. note::

  If you are installing Python on Windows, be sure to check the box to have 
  Python added to your PATH if the installer offers such an option 
  (it's normally off by default).


Installing :mod:`bloxone`
====================================

#. Install from PyPI

The :mod:`bloxone` module is available on PyPI and can simply be installed
using pip/pip3::

  pip3 install bloxone <--user>

#. Intall bloxone as local package from source

If you have downloaded the source from GitHub then :mod:`bloxone` has been 
provided as an installable package using pip.

In your appropriate python3 environment you can therefore install :mod:`bloxone`
using the pip command from the root of the sourcetree. For example::

  pip3 install dist/bloxone-<version>-py3-none-any.whl --user

  or 

  pip3 install dist/bloxone-<version>.tar.gz --user

.. note::

  Use of pip ensures module dependencies and allows for 
  uninstallation and upgrades to be handled cleanly.



Uninstalling :mod:`bloxone`
====================================

You can use pip to unintsall the library. For example::

  pip3 uninstall bloxone
