import hikari
import lightbulb
from lightbulb import slash_commands


class Ping(slash_commands.SlashCommand):
    @property
    def options(self):
        return []

    @property
    def description(self):
        return "Assures that the glorious Quiggle Prime is online."

    @property
    def enabled_guilds(self):
        return None

    async def callback(self, context):
        await context.respond("Pong!", flags=hikari.messages.MessageFlag.EPHEMERAL)


def init(quiggle):
    quiggle.add_slash_command(Ping)
