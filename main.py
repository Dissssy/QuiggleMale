import os
import sys
import config
import hikari
import lightbulb
import importlib
import logging
import models
from sqlalchemy import create_engine

sys.path.append(".")

l = logging.getLogger("main")
l.setLevel(logging.INFO)


def load_module_folder(bot, path: str = "modules"):
    """Load modules from specific path"""
    modules = {}
    here = os.path.dirname(__file__)
    modules_folder = os.path.join(here, path)
    for file in os.listdir(modules_folder):
        if file == "__pycache__":
            continue
        module = importlib.import_module(
            f"{path.replace(os.sep, '.')}.{file.replace('.py', '')}"
        )
        module.init(bot)
        l.info(f"Loaded module {file}")
        modules[file] = module
    return modules


def main():
    quiggle = lightbulb.Bot(token=config.token, slash_commands_only=True)
    quiggle.db = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    models.create_models(quiggle.db)
    quiggle.config = config

    modules = load_module_folder(quiggle)
    quiggle.run(asyncio_debug=True)


if __name__ == "__main__":
    main()
