#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from functools import wraps

import transaction


# Functions & classes =========================================================
def transaction_manager(fn):
    """
    Decorator which wraps whole function into ``with transaction.manager:``.
    """
    @wraps(fn)
    def transaction_manager_decorator(*args, **kwargs):
        with transaction.manager:
            return fn(*args, **kwargs)

    return transaction_manager_decorator
