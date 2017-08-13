"""Python bindings for 0MQ."""

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.

# load bundled libzmq, if there is one:
def _load_libzmq():
    """load bundled libzmq if there is one"""
    import sys, ctypes, platform, os
    dlopen = hasattr(sys, 'getdlopenflags') # unix-only
    # RTLD flags are added to os in Python 3
    # get values from os because ctypes are WRONG on pypy
    if dlopen:
        dlflags = sys.getdlopenflags()
        sys.setdlopenflags(ctypes.RTLD_GLOBAL)
    try:
        from . import libzmq
    except ImportError:
        pass
    else:
        # store libzmq as zmq._libzmq for backward-compat
        globals()['_libzmq'] = libzmq
    finally:
        if dlopen:
            sys.setdlopenflags(dlflags)

_load_libzmq()


# zmq top-level imports

from zmq import backend
from zmq.backend import *
from zmq import sugar
from zmq.sugar import *

def get_includes():
    """Return a list of directories to include for linking against pyzmq with cython."""
    from os.path import join, dirname, abspath, pardir, exists
    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    includes = [ parent ] + [ join(parent, base, subdir) for subdir in ('utils',) ]
    if exists(join(parent, base, 'include')):
        includes.append(join(parent, base, 'include'))
    return includes
    
def get_library_dirs():
    """Return a list of directories used to link against pyzmq's bundled libzmq."""
    from os.path import join, dirname, abspath, pardir
    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    return [ join(parent, base) ]

COPY_THRESHOLD = 65536
__all__ = ['get_includes', 'COPY_THRESHOLD'] + sugar.__all__ + backend.__all__
