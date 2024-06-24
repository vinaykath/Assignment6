"""Testing for an app"""
import pytest
from app import App
from app.command_processor import CommandProcessor


def test_app_get_environment_variable():
    '''Testing app environment variable'''
    app = App()
#   Retrieve the current environment setting
    current_env = app.get_environment_variable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT','TESTING','PRODUCTION'],f"Invalid: {current_env}"



def test_app_start_exit_command(monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    processor = CommandProcessor()
    with pytest.raises(SystemExit):
        processor.process_command(CommandProcessor.Command.EXIT)

def test_app_start_unknown_command(monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    processor = CommandProcessor()
    with pytest.raises(SystemExit):
        processor.process_command(CommandProcessor.Command.UNKNOWN)
