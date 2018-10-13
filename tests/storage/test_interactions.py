# Standard lib imports
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

# Third party imports
# None

# Project level imports
from foosball.storage.interactions import Interactions
from foosball import GAME_TABLES, PLAYERS


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(WhenTestingInteractions())
    return test_suite


class WhenTestingInteractions(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_datetime(self):
        interactions_datetime = Interactions.get_datetime()
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertAlmostEqual(
            interactions_datetime, datetime_now, delta=timedelta(seconds=1)
        )

    def test_clear_color_players_from_table(self):
        with patch.dict(GAME_TABLES,
                        {200: {'status': 'STARTED', 'yellow': 'test2',
                               'black': 'test1', 'yellow_score': 4,
                               'black_score': 0, 'last_to_score': 'yellow',
                               'datetime_last_goal': '2018-10-12 19:48:07'}}):
            with patch.dict(PLAYERS,
                            {
                                'test1': {
                                    'table': 101,
                                    'game_records': [0],
                                    'created': '2018-10-12 19:46:03'
                                },
                                'test2': {
                                    'table': 101,
                                    'game_records': [0],
                                    'created': '2018-10-12 19:46:03'
                                },
                                'test3': {
                                    'table': 0,
                                    'game_records': [],
                                    'created': '2018-10-12 19:46:03'}
                            }):

                self.assertEqual(PLAYERS['test1']['table'], 101)
                self.assertEqual(PLAYERS['test2']['table'], 101)
                self.assertEqual(PLAYERS['test3']['table'], 0)
                Interactions._clear_color_players_from_table(200)
                self.assertEqual(PLAYERS['test1']['table'], 0)
                self.assertEqual(PLAYERS['test2']['table'], 0)
                self.assertEqual(PLAYERS['test3']['table'], 0)

    def test_new_registration_entry(self):
        Interactions.new_registration_entry('test1')
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.assertAlmostEqual(
            PLAYERS['test1']['created'], datetime_now, delta=timedelta(seconds=1)
        )
        self.assertEqual(PLAYERS['test1']['table'], 0)
        self.assertIs(type(PLAYERS['test1']['game_records']), list)
