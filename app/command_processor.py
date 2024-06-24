import os
import importlib.util
from app.plugins.commands import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand

class CommandProcessor:
    def __init__(self):
        self.commands = {'add': AddCommand(),
            'subtract': SubtractCommand(),
            'multiply': MultiplyCommand(),
            'divide': DivideCommand()}
        self.load_commands()

    def load_commands(self):
        commands_dir = os.path.join(os.path.dirname(__file__), 'base_command')
        for filename in os.listdir(commands_dir):
            if filename.endswith('_command.py'):
                command_name = filename[:-3]
                module_name = f'commands.{command_name}'
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(commands_dir, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                command_class = getattr(module, command_name.capitalize())
                self.commands[command_name[:-8]] = command_class()

    def execute_command(self, command_name, *args):
        command = self.commands.get(command_name)
        if not command:
            raise ValueError(f"Command '{command_name}' not found.")
        return command.execute(*args)
    
    class Command:
        EXIT = "exit"
        UNKNOWN = "unknown"

    def process_command(self, command):
        if command == self.Command.EXIT:
            raise SystemExit
        elif command == self.Command.UNKNOWN:
            raise SystemExit
        else:
            print(f"Command {command} processed")
