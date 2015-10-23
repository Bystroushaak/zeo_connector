Introduction
============

.. image:: https://badge.fury.io/py/zeo_connector.png
    :target: https://pypi.python.org/pypi/zeo_connector

.. image:: https://img.shields.io/pypi/dm/zeo_connector.svg
    :target: https://pypi.python.org/pypi/zeo_connector

.. image:: https://img.shields.io/pypi/l/zeo_connector.svg

.. image:: https://img.shields.io/github/issues/Bystroushaak/zeo_connector.svg
    :target: https://github.com/Bystroushaak/zeo_connector/issues

Wrappers, which make working with ZEO_ little bit nicer.

By default, you have to do a lot of stuff, like create connection to database, maintain it, synchronize it (or running asyncore loop), handle reconnects and so on. Classes defined in this project makes all this work for you at the background.

.. _ZEO: http://www.zodb.org/en/latest/documentation/guide/zeo.html

Documentation
-------------

This module defines three classes:

    - ZEOWrapperPrototype
    - ZEOConfWrapper
    - ZEOWrapper

ZEOWrapperPrototype
+++++++++++++++++++
``ZEOWrapperPrototype`` contains methods and shared attributes, which may be used by derived classes.

You can pretty much ignore this class, unless you want to make your own connector.

ZEOConfWrapper
++++++++++++++
``ZEOConfWrapper`` may be used to create connection to ZEO from `XML configuration file <https://pypi.python.org/pypi/ZEO/4.2.0b1#configuring-clients>`_.

Lets say you have file ``/tests/data/zeo_client.conf``:

.. code-block:: python

    <zeoclient>
      server localhost:60985
    </zeoclient>

You can now create the ``ZEOConfWrapper`` object:

.. code-block:: python

    from zeo_connector import ZEOConfWrapper

    db_obj = ZEOConfWrapper(
        conf_path="/tests/data/zeo_client.conf",
        project_key="Some project key",
    )

and save the data to the database:

.. code-block:: python

    import transaction

    with transaction.manager:
        db_obj["data"] = "some data"

String ``"some data"`` is now saved under ``db._connection.root()[project_key]["data"]`` path.

ZEOWrapper
++++++++++
``ZEOWrapper`` doesn't use XML configuration file, but direct server/port specification:

.. code-block:: python

    from zeo_connector import ZEOWrapper

    different_db_obj = ZEOWrapper(
        server="localhost",
        port=60985,
        project_key="Some project key",
    )

So you can retreive the data you stored into the database:

.. code-block:: python

    import transaction

    with transaction.manager:
        print different_db_obj["data"]

Running the ZEO server
----------------------
The examples expects, that the ZEO server is running. To run the ZEO, look at the help page of the ``runzeo`` script which is part of the ZEO bundle. This script requires commandline or XML configuration.

You can generate the configuration files using provided ``zeo_connector_gen_defaults.py`` script, which is part of the `zeo_connector_defaults <https://github.com/Bystroushaak/zeo_connector_defaults>` package::

    $ zeo_connector_gen_defaults.py --help
    usage: zeo_connector_gen_defaults.py [-h] [-s SERVER] [-p PORT] [-C] [-S]
                                         [PATH]

    This program will create the default ZEO XML configuration files.

    positional arguments:
      PATH                  Path to the database on the server (used in server
                            configuration only.

    optional arguments:
      -h, --help            show this help message and exit
      -s SERVER, --server SERVER
                            Server url. Default: localhost
      -p PORT, --port PORT  Port of the server. Default: 60985
      -C, --only-client     Create only CLIENT configuration.
      -S, --only-server     Create only SERVER configuration

For example::

    $ zeo_connector_gen_defaults.py /tmp

will create ``zeo.conf`` file with following content:

.. code-block:: xml

    <zeo>
      address localhost:60985
    </zeo>

    <filestorage>
      path /tmp/storage.fs
    </filestorage>

    <eventlog>
      level INFO
      <logfile>
        path /tmp/zeo.log
        format %(asctime)s %(message)s
      </logfile>
    </eventlog>

and ``zeo_client.conf`` containing:

.. code-block:: xml

    <zeoclient>
      server localhost:60985
    </zeoclient>

You can change the ports and address of the server using ``--server`` or ``--port`` arguments.

To run the ZEO with the server configuration file, run the following command::

    runzeo -C zeo.conf

To run the client, you may use ``ZEOConfWrapper``, as was show above:

.. code-block:: python

    from zeo_connector import ZEOConfWrapper

    db_obj = ZEOConfWrapper(
        conf_path="./zeo_client.conf",
        project_key="Some project key",
    )

Installation
------------

Module is `hosted at PYPI <https://pypi.python.org/pypi/zeo_connector>`_, and can be easily installed using `PIP`_::

    sudo pip install zeo_connector

.. _PIP: http://en.wikipedia.org/wiki/Pip_%28package_manager%29


Source code
-----------

Project is released under the MIT license. Source code can be found at GitHub:

- https://github.com/Bystroushaak/zeo_connector

Unittests
---------

You can run the tests using provided ``run_tests.sh`` script, which can be found in the root of the project.

If you have any trouble, just add ``--pdb`` switch at the end of your ``run_tests.sh`` command like this: ``./run_tests.sh --pdb``. This will drop you to `PDB`_ shell.

.. _PDB: https://docs.python.org/2/library/pdb.html

Requirements
++++++++++++
This script expects that package pytest_ is installed. In case you don't have it yet, it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/

Example
+++++++

::

    $ ./run_tests.sh 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.30 -- pytest-2.7.2
    rootdir: /home/bystrousak/Plocha/Dropbox/c0d3z/python/libs/zeo_connector, inifile: 
    plugins: cov
    collected 7 items 

    tests/test_zeo_connector.py .......

    =========================== 7 passed in 7.08 seconds ===========================
