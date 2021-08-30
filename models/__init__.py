import json
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class GameState(Base):
    __tablename__ = "gamestate"

    game_id = Column(Integer, primary_key=True)
    game_type = Column(String)
    state = Column(String)
    players = Column(String)

    def __init__(self, game_type, state=None, players=None):
        self.game_type = game_type
        self.state = json.dumps(state)
        self.players = json.dumps(players)


def create_models(engine):
    Base.metadata.create_all(engine)
