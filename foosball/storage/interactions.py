# Standard lib imports
from datetime import datetime
from operator import itemgetter

# Project-level imports
from foosball import PLAYERS, GAME_TABLES, GAME_RECORDS, \
    TABLE_STATUS_WAITING, TABLE_STATUS_STARTED, TABLE_STATUS_COMPLETED


class Interactions(object):
    """
    Handles player and game table interactions
    """

    @staticmethod
    def get_table_status(table_num):
        return GAME_TABLES[int(table_num)]

    @staticmethod
    def get_game_record(name):
        if len(PLAYERS[name]['game_records']) == 0:
            return {}

        return itemgetter(*PLAYERS[name]['game_records'])(GAME_RECORDS)

    @staticmethod
    def check_if_active_match(table_num):
        if GAME_TABLES[table_num]['status'] == TABLE_STATUS_STARTED:
            return True

        return False

    @staticmethod
    def record_goal(table_num, color):
        winner = ''
        yellow_score = GAME_TABLES[table_num]['yellow_score']
        black_score = GAME_TABLES[table_num]['black_score']

        if color == 'yellow':
            yellow_score += 1
        else:
            black_score += 1

        GAME_TABLES[table_num]['yellow_score'] = yellow_score
        GAME_TABLES[table_num]['black_score'] = black_score
        GAME_TABLES[table_num]['last_to_score'] = color
        GAME_TABLES[table_num]['datetime_last_goal'] = \
            Interactions.get_datetime()
        player1 = GAME_TABLES[table_num]['yellow']
        player2 = GAME_TABLES[table_num]['black']

        # If anyone is at 5 points the game is over
        if yellow_score == 5:
            winner = 'yellow'
        if black_score == 5:
            winner = 'black'

        match_status = GAME_TABLES[table_num]['status']

        if winner:
            GAME_TABLES[table_num]['status'] = TABLE_STATUS_COMPLETED
            match_status = TABLE_STATUS_COMPLETED
            # Record this to the game recorder
            Interactions._add_new_game_record(table_num, winner)
            del GAME_TABLES[table_num]

        return match_status, yellow_score, black_score

    @staticmethod
    def new_registration_entry(name):
        new_player = {
            'table': 0,
            'game_records': [],
            'created': Interactions.get_datetime()
        }

        PLAYERS[name] = new_player

    @staticmethod
    def new_table_entry(table_num, name, color):
        # If they are in any other table that game is now abandoned
        Interactions._abandon_table(name, table_num)

        new_table = {
            'status': TABLE_STATUS_WAITING,
            'yellow': '',
            'black': '',
            'yellow_score': 0,
            'black_score': 0,
            'last_to_score': '',
            'datetime_last_goal': ''
        }

        if color == "yellow":
            new_table['yellow'] = name
        else:
            new_table['black'] = name

        GAME_TABLES[table_num] = new_table

        # Update player to the new table
        PLAYERS[name]['table'] = table_num

        return TABLE_STATUS_WAITING

    @staticmethod
    def join_existing_table(table_num, name, color):
        # The rule is if they overwrite a color when joining the table, the
        # current game is considered abandoned
        status = GAME_TABLES[table_num]['status']

        if status == TABLE_STATUS_STARTED:
            # They joined a table with a started game
            Interactions._clear_color_players_from_table(table_num)
            return Interactions._delete_and_recreate_table(
                table_num, name, color)

        # If they are in any other table that game is now abandoned
        Interactions._abandon_table(name, table_num)

        # Is there an opponent?
        try:
            if color == 'black':
                opponent = GAME_TABLES[table_num]['yellow']
            else:
                opponent = GAME_TABLES[table_num]['black']
        except KeyError:
            # This scenario happens when they are in a table by themselves
            # and they change colors
            return Interactions._delete_and_recreate_table(
                table_num, name, color)

        # Check if they are joining a table that exists and taking someone
        # else's color
        if len(opponent) == 0 and status == TABLE_STATUS_WAITING:
            # Get the opponent's name being overwritten and set their room to 0
            PLAYERS[GAME_TABLES[table_num][color]]['table'] = 0

        if len(opponent) > 0 and status == TABLE_STATUS_WAITING:
            # Change the game status to started
            GAME_TABLES[table_num]['status'] = TABLE_STATUS_STARTED
            status = TABLE_STATUS_STARTED

        GAME_TABLES[table_num][color] = name
        # Update player to the new table
        PLAYERS[name]['table'] = table_num

        return status

    @staticmethod
    def _delete_and_recreate_table(table_num, name, color):
        # Rather than clean out individual values just delete the table and
        # build a fresh one with default settings
        if table_num in GAME_TABLES:
            del GAME_TABLES[table_num]

        return Interactions.new_table_entry(table_num, name, color)

    @staticmethod
    def _abandon_table(name, table_num):
        prior_table_num = PLAYERS[name]['table']

        if table_num in GAME_TABLES and prior_table_num != 0 \
                and prior_table_num != table_num:
            Interactions._clear_color_players_from_table(table_num)
        if prior_table_num in GAME_TABLES:
            del GAME_TABLES[prior_table_num]

    @staticmethod
    def _clear_color_players_from_table(table_num):
        for color in ['yellow', 'black']:
            color_name = GAME_TABLES[table_num][color]

            if len(color_name) > 0:
                PLAYERS[color_name]['table'] = 0

    @staticmethod
    def _add_new_game_record(table_num, winner):
        table = GAME_TABLES[table_num]

        if winner == 'yellow':
            opponent = 'black'
        else:
            opponent = 'yellow'

        match_data = {
            'winner': table[winner],
            'winner_score': 5,
            'opponent': table[opponent],
            'opponent_score': table[opponent + '_score'],
            'datetime_completed': Interactions.get_datetime(),
            'table_num': table_num
        }

        GAME_RECORDS.append(match_data)
        # Record the index to the player's registration game records
        for name in [table[winner], table[opponent]]:
            PLAYERS[name]['game_records'].append(len(GAME_RECORDS) - 1)

    @staticmethod
    def get_datetime():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
