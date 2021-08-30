import os
import config
import hikari
import lightbulb
import importlib
import logging
import models
from sqlalchemy import create_engine

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

quiggle = lightbulb.Bot(token=config.token, prefix="something")
modules = load_module_folder(quiggle)

quiggle.db = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

models.create_models(quiggle.db)

quiggle.run(asyncio_debug=True)
