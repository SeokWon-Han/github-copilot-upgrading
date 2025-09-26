#!python
"""Bootstrap distribute installation

If you want to use setuptools in your package's setup.py, just include this
file in the same directory with it, and add this to the top of your setup.py::

    from distribute_setup import use_setuptools
    use_setuptools()

If you want to require a specific version of setuptools, set a download
mirror, or use an alternate download directory, you can do so by supplying
the appropriate options to ``use_setuptools()``.

This file can also be run as a script to install or upgrade setuptools.
"""
import os
import sys
import time
import fnmatch
import tempfile
import tarfile
from distutils import log

try:
    from site import USER_SITE
except ImportError:
    USER_SITE = None

try:
    import subprocess

    def _python_cmd(*args):
        args = (sys.executable,) + args
        return subprocess.call(args) == 0

except ImportError:
    # will be used for python 2.3
    def _python_cmd(*args):
        args = (sys.executable,) + args
        # quoting arguments if windows
        if sys.platform == 'win32':
            def quote(arg):
                if ' ' in arg:
                    return '"%s"' % arg
                return arg
            args = [quote(arg) for arg in args]
        return os.spawnl(os.P_WAIT, sys.executable, *args) == 0

DEFAULT_VERSION = "0.6.10"
DEFAULT_URL = "http://pypi.python.org/packages/source/d/distribute/"
SETUPTOOLS_FAKED_VERSION = "0.6c11"

SETUPTOOLS_PKG_INFO = """\
Metadata-Version: 1.0
Name: setuptools
Version: %s
Summary: xxxx
Home-page: xxx
Author: xxx
Author-email: xxx
License: xxx
Description: xxx
""" % SETUPTOOLS_FAKED_VERSION
