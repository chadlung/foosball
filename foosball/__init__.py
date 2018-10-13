# This data would normally be tracked in a datastore like
# MongoDB, Postgres, etc. However for this exercise the focus
# is on the code versus a backend datastore. Keep in mind when running
# this REST service it is expected the calls come in one at a time to
# preserve the integrity of the dicts, lists below.
GAME_TABLES = {}
PLAYERS = {}
GAME_RECORDS = []

TABLE_STATUS_WAITING = 'WAITING'
TABLE_STATUS_COMPLETED = 'COMPLETED'
TABLE_STATUS_STARTED = 'STARTED'
