# Third-party imports
import falcon

# Project-level imports
from foosball.storage.interactions import Interactions


class TableResource(object):

    def on_get(self, req, resp, table_num):
        resp.status = falcon.HTTP_BAD_REQUEST
        resp.media = {"Error": "Invalid table number"}

        try:
            if not isinstance(table_num, int):
                resp.media = {"Error": "Invalid table number"}
                return
        except KeyError:
            return

        try:
            resp.media = Interactions.get_table_status(table_num)
            resp.status = falcon.HTTP_200
            return
        except KeyError:
            resp.media = {"Error": "The table number specified doesn't exist"}
