#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import time
import os.path
from functools import wraps

from ZODB import DB
from ZODB.config import storageFromFile
from ZODB.POSException import ConnectionStateError

from BTrees.OOBTree import OOBTree


# Variables ===================================================================
PROJECT_KEY = "pAPI"
_CONNECTION = None  #: Cache for calls to :meth:`get_zeo_connection`.


# Functions & classes =========================================================
def use_new_connection():
    """
    Use new connection to ZEO.
    """
    global _CONNECTION

    if _CONNECTION:
        _CONNECTION.sync()
        _CONNECTION.close()

    _CONNECTION = None


def get_zeo_connection(cached=True, on_close_callback=use_new_connection):
    """
    Return connection to the database. You can get root of the database from
    this connection.

    Warning:
        Don't try to put one object into multiple connections. It won't work.

    Args:
        cached (bool, default True): Use cached connection to database.
        on_close_callback (fn pointer, default None): Function which should be
                          used when the connection is closed.

    Returns:
        obj: ZODB connection object.
    """
    global _CONNECTION
    if _CONNECTION and cached:
        _CONNECTION.sync()  # pull invalidation queue
        return _CONNECTION

    path = os.path.join(os.path.dirname(__file__), "zeo_client.conf")

    # check whether there is zeo_client conf in user's home directory
    home_conf_path = os.path.expanduser("~/.pAPI/zeo_client.conf")
    if os.path.exists(home_conf_path):
        path = home_conf_path

    storage = storageFromFile(open(path))
    db = DB(storage)
    connection = db.open()

    if on_close_callback:
        connection.onCloseCallback(on_close_callback)

    if cached:
        _CONNECTION = connection

    return connection


def get_zeo_root(cached=True):
    """
    Return :attr:`.PROJECT_KEY` from the root of the database.

    Args:
        cached (bool, default True): Cache connection. This will prevent nasty
               problems with putting same object into multiple connections.

    Returns:
        OOBTree: Project key from the root of the database.
    """
    conn = get_zeo_connection()

    try:
        dbroot = conn.root()
    except ConnectionStateError:
        if cached:
            return get_zeo_root(cached=False)

        raise

    if PROJECT_KEY not in dbroot:
        dbroot[PROJECT_KEY] = OOBTree()

    return dbroot[PROJECT_KEY]


def get_zeo_key(key, new_obj=OOBTree, cached=True):
    """
    Get key from the PROJECT_KEY root. Use `new_type` as the new type of the
    key, if not found.

    Args:
        key (str): Name of the key which will be returned from the root.
        new_type (obj, default OOBTree): Put `new_type` into key if the key
                 wasn't found.
        cached (bool, default True): Use cached connection - good for writing,
               but don't use this for reading, or you will get unupdated view
               to database.

    Returns:
        obj: Object at `key`. `new_type` instance if not found.
    """
    root = get_zeo_root(cached=cached)

    if not root.get(key, None):
        root[key] = new_obj()

    return root[key]


def cached_connection(fn=None, timeout=10):
    """
    Decorator to automatically call `use_new_connection` after `timeout` (in
    seconds).
    """
    def cached_connection_decorator(fn):
        # list is used because can be changed without global definition
        last_time = [time.time()]

        @wraps(fn)
        def cached_connection_wrapper(*args, **kwargs):
            if time.time() > (last_time[0] + timeout):
                use_new_connection()
                last_time[0] = time.time()

            return fn(*args, **kwargs)

        return cached_connection_wrapper

    if fn:  # python decorator with optional parameters bukkake
        return cached_connection_decorator(fn)

    return cached_connection_decorator
