import hikari
from lightbulb import slash_commands
import config


class Ping(slash_commands.SlashCommand):
    def __init__(self, bot):
        self._enabled_guilds = bot.config.enabled_guilds
        super().__init__(bot)

    @property
    def options(self):
        return []

    @property
    def description(self):
        return "Assures that the glorious Quiggle Prime is online."

    @property
    def enabled_guilds(self):
        return config.enabled_guilds

    async def callback(self, context):
        await context.respond(
            "Pong!", flags=hikari.messages.MessageFlag.EPHEMERAL, components=[])


def init(quiggle):
    quiggle.add_slash_command(Ping)
