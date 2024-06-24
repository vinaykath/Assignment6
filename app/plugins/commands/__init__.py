import logging
from app.base_command import Command

class AddCommand(Command):
    def execute(self, *args):
        logging.info("Addition")
        return sum(args)

class SubtractCommand(Command):
    def execute(self, *args):
        result = args[0]
        for num in args[1:]:
            result -= num
        return result

class MultiplyCommand(Command):
    def execute(self, *args):
        result = 1
        for num in args:
            result *= num
        return result

class DivideCommand(Command):
    def execute(self, *args):
        result = args[0]
        for num in args[1:]:
            result /= num
        return result