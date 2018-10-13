# Third-party imports
import falcon
from falcon.media.validators.jsonschema import validate

# Project-level imports
from foosball.schemas import load_schema
from foosball import GAME_TABLES
from foosball.storage.interactions import Interactions


class GoalResource(object):
    # Record each goal's data: the scoring player, their opponent, the table,
    # the time of the goal

    @validate(load_schema('goal'))
    def on_post(self, req, resp):
        table_num = req.media.get('table')
        color = req.media.get('color')

        resp.status = falcon.HTTP_BAD_REQUEST

        if table_num not in GAME_TABLES:
            # The table num doesn't exist
            resp.media = {"Error": "The table number specified doesn't exist"}
            return

        # Check if the table is in a match
        if not Interactions.check_if_active_match(table_num):
            resp.media = {"Error": "The table number is not in an active game"}
            return

        # Record the goal
        match_status, yellow_score, black_score = \
            Interactions.record_goal(table_num, color)

        resp.media = {
            "status": match_status,
            "yellow_score": yellow_score,
            "black_score": black_score
        }
        resp.status = falcon.HTTP_200
