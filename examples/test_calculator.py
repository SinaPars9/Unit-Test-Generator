import pytest
from calculator import divide


def test_divide_normal():
    assert divide(10, 2) == 5


def test_divide_negative():
    assert divide(-10, 2) == -5


def test_divide_float():
    assert divide(7, 2) == 3.5


def test_divide_float_numbers():
    assert divide(1.5, 0.5) == 3.0


def test_divide_zero_numerator():
    assert divide(0, 5) == 0


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_divide_by_zero_raises_value_error_negative():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(-5, 0)