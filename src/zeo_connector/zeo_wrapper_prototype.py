#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import thread
import asyncore
from functools import wraps

import transaction
from ZODB.POSException import ConnectionStateError
from BTrees.OOBTree import OOBTree


# Variables ===================================================================
_ASYNCORE_RUNNING = False


# Functions & classes =========================================================
def _init_zeo():
    """
    Start asyncore thread.
    """
    if not _ASYNCORE_RUNNING:
        def _run_asyncore_loop():
            asyncore.loop()

        thread.start_new_thread(_run_asyncore_loop, ())

        global _ASYNCORE_RUNNING
        _ASYNCORE_RUNNING = True


def retry_and_reset(fn):
    """
    Decorator used to make sure, that operation on ZEO object will be retried,
    if there is ``ConnectionStateError`` exception.
    """
    @wraps(fn)
    def retry_and_reset_decorator(*args, **kwargs):
        obj = kwargs.get("self", None)

        if not obj:
            obj = args[0]

        try:
            return fn(*args, **kwargs)
        except ConnectionStateError:
            obj._on_close_callback()

        return fn(*args, **kwargs)

    return retry_and_reset_decorator


class ZEOWrapperPrototype(object):
    """
    ZEO wrapper prototype baseclass.

    Attributes:
        project_key (str): Project key, under which will this object access the
            ZEO structure.
        default_type (obj): Default data object used for root, if the root
            wasn't already created in ZEO.
    """
    def __init__(self, project_key=None, run_asyncore_thread=True):
        """
        Initialize the object.

        Args:
            conf_path (str): See :attr:`conf_path`.
            project_key (str, default None): See :attr:`project_key`. If not
                set, the root of the database is used (this may cause
                performace issues).
            run_asyncore_thread (bool, default True): Run external asyncore
                thread, which handles connections to database? Default True.
        """
        self.project_key = project_key
        self.default_type = OOBTree

        self._root = None  #: Reference to the root of the database.
        self._connection = None  #: Internal handler for the ZEO connection.

        if run_asyncore_thread:
            _init_zeo()

        self._open_connection()
        self._init_zeo_root()

    def _on_close_callback(self):
        """
        When the connection is closed, open it again and get new reference to
        ZEO root.
        """
        self._open_connection()
        self._init_zeo_root()

    def _get_db(self):
        """
        This should return the ZODB database object.
        """
        raise NotImplementedError("._get_db() is not implemented yet.")

    def _open_connection(self):
        """
        Open the connection to the database based on the configuration file.
        """
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass

        db = self._get_db()
        self._connection = db.open()

        self._connection.onCloseCallback(self._on_close_callback)

    def _init_zeo_root(self, attempts=3):
        """
        Get and initialize the ZEO root object.

        Args:
            attempts (int, default 3): How many times to try, if the connection
                was lost.
        """
        try:
            db_root = self._connection.root()
        except ConnectionStateError:
            if attempts <= 0:
                raise

            self._open_connection()
            return self._init_zeo_root(attempts=attempts-1)

        # init the root, if it wasn't already declared
        if self.project_key and self.project_key not in db_root:
            with transaction.manager:
                db_root[self.project_key] = self.default_type()

        self._root = db_root[self.project_key] if self.project_key else db_root

    def sync(self):
        """
        Sync the connection.

        Warning:
            Don't use this method, if you are in the middle of transaction, or
            the transaction will be aborted.

        Note:
            You don't have to use this when you set :attr:`run_asyncore_thread`
            to ``True``.
        """
        self._connection.sync()

    @retry_and_reset
    def __getitem__(self, key):
        return self._root[key]

    @retry_and_reset
    def __setitem__(self, key, val):
        self._root[key] = val

    @retry_and_reset
    def __contains__(self, key):
        return key in self._root

    @retry_and_reset
    def __delitem__(self, key):
        del self._root[key]

    @retry_and_reset
    def __iter__(self):
        return self._root.iteritems()

    @retry_and_reset
    def iteritems(self):
        return self._root.iteritems()

    @retry_and_reset
    def keys(self):
        return self._root.keys()

    @retry_and_reset
    def iterkeys(self):
        return self._root.iterkeys()

    @retry_and_reset
    def values(self):
        return self._root.values()

    @retry_and_reset
    def itervalues(self):
        return self._root.itervalues()

    @retry_and_reset
    def get(self, key, alt):
        return self._root.get(key, alt)

    def pack(self):
        """
        Call .pack() on the database (transaction history cleanup).
        """
        return self._get_db().pack()
