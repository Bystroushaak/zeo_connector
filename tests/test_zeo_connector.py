#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

import transaction

from zeo_connector import ZEOWrapper
from zeo_connector import ZEOConfWrapper

import environment_generator


# Variables ===================================================================
PROJECT_KEY = "some_key"


# Setup =======================================================================
def setup_module(module):
    environment_generator.generate_environment()


def teardown_module(module):
    environment_generator.cleanup_environment()


# Fixtures ====================================================================
@pytest.fixture
def zeo_conf_wrapper():
    return ZEOConfWrapper(
        conf_path=environment_generator.tmp_context_name("zeo_client.conf"),
        project_key=PROJECT_KEY,
    )


@pytest.fixture
def zeo_wrapper():
    return ZEOWrapper(
        server="localhost",
        port=60985,
        project_key=PROJECT_KEY,
    )


# Tests =======================================================================
def test_zeo_conf_wrapper_storing_and_retreiving():
    first_wrapper = zeo_conf_wrapper()
    second_wrapper = zeo_conf_wrapper()

    with transaction.manager:
        first_wrapper["something"] = "hello"
        assert first_wrapper["something"] == "hello"

    with transaction.manager:
        assert second_wrapper["something"] == "hello"


def test_zeo_conf_wrapper_storing(zeo_conf_wrapper):
    with transaction.manager:
        zeo_conf_wrapper["azgabash"] = "hello"


def test_zeo_conf_wrapper_retreiving(zeo_conf_wrapper):
    with transaction.manager:
        assert zeo_conf_wrapper["azgabash"] == "hello"


def test_zeo_wrapper_retreiving(zeo_wrapper):
    with transaction.manager:
        assert zeo_wrapper["azgabash"] == "hello"


def test_zeo_wrapper_storing(zeo_wrapper):
    with transaction.manager:
        zeo_wrapper["zeo"] = "hello ZEO"


def test_zeo_wrapper_retreiving_again(zeo_wrapper):
    with transaction.manager:
        assert zeo_wrapper["zeo"] == "hello ZEO"


def test_dict_methods(zeo_wrapper, zeo_conf_wrapper):
    with transaction.manager:
        zeo_wrapper["first"] = 1

    used = {
        "something": "hello",
        "azgabash": "hello",
        "zeo": "hello ZEO",
        "first": 1,
    }

    with transaction.manager:
        assert "first" in zeo_conf_wrapper
        assert zeo_conf_wrapper.get("first", None) == 1
        assert zeo_conf_wrapper.get("second", 2) == 2

        assert set(zeo_conf_wrapper.keys()) == set(used.keys())
        assert set(zeo_conf_wrapper.values()) == set(used.values())

        assert set(zeo_conf_wrapper.iterkeys()) == set(used.iterkeys())
        assert set(zeo_conf_wrapper.itervalues()) == set(used.itervalues())

        iterated = {
            key: val
            for key, val in zeo_conf_wrapper
        }

        assert iterated == used

    with transaction.manager:
        del zeo_conf_wrapper["first"]

    with transaction.manager:
        assert "first" not in zeo_wrapper
