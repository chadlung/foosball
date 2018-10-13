# Standard lib imports
import falcon


class VersionResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'version': '1.0.0'
        }
