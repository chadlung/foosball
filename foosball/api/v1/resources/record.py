# Third-party imports
import falcon

# Project-level imports
from foosball import PLAYERS
from foosball.storage.interactions import Interactions


class RecordResource(object):

    def on_get(self, req, resp, name):
        resp.status = falcon.HTTP_BAD_REQUEST

        if name not in PLAYERS:
            # The name doesn't exist
            resp.media = {"Error": "The name specified doesn't exist"}
            return

        # Fetch the game record data for the name
        resp.media = Interactions.get_game_record(name)
        resp.status = falcon.HTTP_200
