# Quiggle Prime

Quiggle Prime is a Discord bot about tiny minigames. It is written in Python 3.9, and uses [hikari](https://github.com/hikari-py/hikari) and [hikari-lightbulb](https://github.com/tandemdude/hikari-lightbulb).

This is a rewrite of [Quiggle](https://github.com/Dissssy/QuiggleMale/tree/master).

## Installation

```sh
# <optional, but preferred: choose your favorite env manager>
python -m pip install .
cp config.template.py config.py
$EDITOR config.py
python main.py
```

The bot uses Discord's slash commands. When you invite it, make sure to include both `bot` and `applications.commands` in the scope.
