import os
import pkgutil
import importlib
# from commands import Command, CommandHandler
from .command_processor import CommandProcessor
from dotenv import load_dotenv
import logging
import logging.config
import importlib.util

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        # self.command_handler = CommandHandler()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, CommandProcessor.Command) and item is not CommandProcessor.Command:
                # Command names are now explicitly set to the plugin's folder name
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        self.load_plugins()
        processor = CommandProcessor()
        logging.info("Application started. Type 'exit' to exit.")
        environment = os.getenv("ENVIRONMENT", "development")
        self.logger.info(f"Running in {environment} environment")

        print("Available commands: add, subtract, multiply, divide, menu, exit")
        
        while True:
            user_input = input("Enter command: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'menu':
                print("Available commands: add, subtract, multiply, divide, menu, exit")
                continue
            parts = user_input.split()
            command_name = parts[0]
            args = []
            for part in parts[1:]:
                try:
                    args.append(float(part))
                except ValueError as e:
                    raise ValueError(f"Could not convert string to float: '{part}'") from e
            try:
                result = processor.execute_command(command_name, *args)
                self.logger.info(f"Executed command: {command_name} with arguments {args}. Result: {result}")
                print(f"Result: {result}")
            except ValueError as e:
                self.logger.error(f"ValueError: {e}")
                print(e)
            except Exception as e:
                self.logger.error(f"Exception: {e}")
                print(f"An error occurred: {e}")
            finally:
                logging.info("Application shutdown.")


if __name__ == "__main__":
    app = App()
    app.start()
