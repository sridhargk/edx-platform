""" Tests for the utility decorators for Paver """
import time

import pytest

from pavelib.utils.decorators import (
    timeout, TimeoutException
)


def test_function_under_timeout():

    @timeout(5)
    def sample_function_1():
        time.sleep(3)
        return "sample text"

    value = sample_function_1()
    assert value == "sample text"


def test_function_over_timeout():

    @timeout(3)
    def sample_function_2():
        time.sleep(5)
        return "sample text"

    with pytest.raises(TimeoutException):
        value = sample_function_2()
        assert value == "sample text"
