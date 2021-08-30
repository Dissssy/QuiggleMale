import hikari
from lightbulb import slash_commands
import config


class TicTacToe(slash_commands.SlashCommand):
    @property
    def options(self):
        return [
            hikari.CommandOption(
                name="player",
                description="Your opponent",
                type=hikari.OptionType.USER,
                is_required=True,
            )
        ]

    @property
    def description(self):
        return "Challenge an opponent to a game of Tic-Tac-Toe."

    @property
    def enabled_guilds(self):
        return config.enabled_guilds

    async def callback(self, context):
        print(type(context.member))
        print(type(context.user))
        await context.respond("`raise NotImplementedError`")


def init(quiggle):
    quiggle.add_slash_command(TicTacToe)
