
============================
How to make a python package
============================
https://python-packaging.readthedocs.io/en/latest/minimal.html


=========================================
How to install the python package locally
=========================================
From the root directory open a commandline and then run the pip command below.
This will install the package within the python installation on the current
machine for the current user.
  >pip install .


=================================
How to uninstall a python package
=================================
  >pip uninstall pyqhtools


==================================
How to upload your package to PyPi
==================================
Create an account on PyPi.
Register your package and upload the relevant metadata by running this:
  >python setup.py register
If you want to upload your package to PyPi so people can install it directly
from there instead of needing to go and clone it from github, then you can use
the following command to register, zip, and upload the package to PyPi in one
step:
  >python setup.py register sdist upload


=========================================
How to install a python package from PyPi
=========================================
C:\blah\PyQhtools\>pip install pyqhtools
