# Third-party imports
import falcon
from falcon.media.validators.jsonschema import validate

# Project-level imports
from foosball.schemas import load_schema
from foosball import PLAYERS, GAME_TABLES
from foosball.storage.interactions import Interactions


class RegistrationResource(object):

    @validate(load_schema('registration'))
    def on_post(self, req, resp):
        name = req.media.get('name')
        table_num = req.media.get('table')
        color = req.media.get('color')

        # Check if name already exists
        if name not in PLAYERS:
            Interactions.new_registration_entry(name)

        if table_num not in GAME_TABLES:
            # The table num doesn't exist
            status = Interactions.new_table_entry(table_num, name, color)
        else:
            status = Interactions.join_existing_table(
                table_num, name, color)

        resp.media = {"status": status}
        resp.status = falcon.HTTP_201
