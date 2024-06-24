'''Test all commands'''
import pytest
from app.command_processor import CommandProcessor

def test_add_command():
    '''Test add command'''
    processor = CommandProcessor()
    assert processor.execute_command('add', 1, 2, 3) == 6

def test_subtract_command():
    '''Test subtract command'''
    processor = CommandProcessor()
    assert processor.execute_command('subtract', 10, 5, 2) == 3

def test_multiply_command():
    '''Test multiply command'''
    processor = CommandProcessor()
    assert processor.execute_command('multiply', 2, 3, 4) == 24

def test_divide_command():
    '''Test divide command'''
    processor = CommandProcessor()
    assert processor.execute_command('divide', 8, 2, 2) == 2

def test_divide_by_zero():
    '''Test divide by zero'''
    processor = CommandProcessor()
    with pytest.raises(ZeroDivisionError):
        processor.execute_command('divide', 8, 0)

def test_invalid_command():
    '''Test invalid command'''
    processor = CommandProcessor()
    with pytest.raises(ValueError):
        processor.execute_command('invalid', 1, 2)

if __name__ == "__main__":
    pytest.main()
