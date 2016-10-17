Changelog
=========

0.4.6
-----
    - Cleanup of metadata files.

0.4.0 - 0.4.5
-------------
    - Added ``@retry_and_reset`` decorator for all internal dict-methods calls.
    - Project key is now optional, so this object may be used to access the root of the database.
    - Property ``ASYNCORE_RUNNING`` renamed to ``_ASYNCORE_RUNNING``.
    - Implemented ``.pack()``.
    - Added ``@transaction_manager``.
    - Added ``examples/database_handler.py`` and tests.
    - Added @wraps(fn) to decorators.
    - Added requirement for zope.interface.
    - Attempt to solve https://github.com/WebArchivCZ/WA-KAT/issues/86

0.3.0
-----
    - Environment generator and other shared parts moved to https://github.com/Bystroushaak/zeo_connector_defaults
    - README.rst improved, added more documentation and additional sections.

0.2.0
-----
    - Added standard dict methods, like ``.__contains__()``, ``.__delitem__()``, ``.__iter__()`` and so on.

0.1.0
-----
    - Project created.
