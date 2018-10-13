"""
Foosball API Service
"""

# Standard lib imports
from wsgiref import simple_server

# Third-party imports
import falcon

# Project-level imports
from foosball.api.v1.resources import goal
from foosball.api.v1.resources import record
from foosball.api.v1.resources import table
from foosball.api.v1.resources import registration
from foosball.api.v1.resources import version


def main():
    base_v1_route = '/api/v1'

    # Resources
    record_res = record.RecordResource()
    table_res = table.TableResource()
    goal_res = goal.GoalResource()
    registration_res = registration.RegistrationResource()
    version_res = version.VersionResource()

    #  Routes
    app.add_route(base_v1_route + '/version', version_res)
    app.add_route(base_v1_route + '/registration', registration_res)
    app.add_route(base_v1_route + '/goal', goal_res)
    app.add_route(base_v1_route + '/record/{name}', record_res)
    app.add_route(base_v1_route + '/table/{table_num}', table_res)

    # For simplicity just using the wsgiref server - note that this is not
    # a production grade server, use Gunicorn or uWSGI instead.
    httpd = simple_server.make_server('127.0.0.1', 8080, app)
    print("Starting server on 127.0.0.1:8080")
    httpd.serve_forever()


app = falcon.API(middleware=[])


if __name__ == '__main__':
    main()
