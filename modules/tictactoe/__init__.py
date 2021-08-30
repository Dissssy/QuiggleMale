import hikari
from lightbulb import slash_commands


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
        return None

    async def callback(self, context):
        print(context.options["player"].value)
        await context.respond("`raise NotImplementedError`")


def init(quiggle):
    quiggle.add_slash_command(TicTacToe)
