import unittest
import datetime, zoneinfo
from timesheet_util import util

class TestMeasureOverlapTimedelta(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(seconds=28480)),
                # argument order switched
                (datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(seconds=28480)),
                # inclusion
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 9, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(seconds=28610)),
                # no overlaps
                (datetime.datetime(2025, 12, 31, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2025, 12, 31, 9, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(hours=0)),
                # timezone
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/Chicago")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/Chicago")),
                 datetime.timedelta(seconds=24880)),
                # timezone, inclusion
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/Chicago")),
                 datetime.datetime(2026, 1, 1, 7, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(seconds=21410)),
                ]

        for a, b, c, d, expected in cases:
            with self.subTest(a=a, b=b, c=c, d=d):
                self.assertEqual(util.measure_overlap_timedelta(a, b, c, d), expected)

class TestMeasureOverlap(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 28480 / 28800),
                # argument order switched
                (datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 28480 / 28610),
                # no overlaps
                (datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2025, 1, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 5, 20, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 8, 2, 10, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 0.0 / 28800),
                ]

        for a, b, c, d, expected in cases:
            with self.subTest(a=a, b=b, c=c, d=d):
                self.assertEqual(util.measure_overlap(a, b, c, d), expected)

class TestIsInCheckInWindow(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2025, 12, 31, 23, 55, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 True),
                # late
                (datetime.datetime(2026, 1, 1, 0, 0, 1, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 False),
                # early
                (datetime.datetime(2025, 12, 31, 23, 25, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 False),
                # edge
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 True),
                ]

        for a, b, c, expected in cases:
            with self.subTest(a=a, b=b, c=c):
                self.assertEqual(util.is_in_check_in_window(a, b, c), expected)

class TestIsInCheckOutWindow(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2026, 1, 1, 0, 0, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 True),
                # early
                (datetime.datetime(2025, 12, 31, 23, 55, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 False),
                # late
                (datetime.datetime(2026, 1, 1, 0, 30, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 False),
                # edge
                (datetime.datetime(2026, 1, 1, 0, 30, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 True),
                ]

        for a, b, c, expected in cases:
            with self.subTest(a=a, b=b, c=c):
                self.assertEqual(util.is_in_check_out_window(a, b, c), expected)

class TestCheckInTime(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2025, 12, 31, 23, 55, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # edge
                (datetime.datetime(2025, 12, 31, 23, 30, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # early
                (datetime.datetime(2025, 12, 31, 23, 29, 59, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2025, 12, 31, 23, 29, 59, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # late
                (datetime.datetime(2026, 1, 1, 0, 0, 1, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 1, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                ]

        for a, b, c, expected in cases:
            with self.subTest(a=a, b=b, c=c):
                self.assertEqual(util.check_in_time(a, b, c), expected)

class TestCheckOutTime(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2026, 1, 1, 0, 0, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # edge
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 30, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # early
                (datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2025, 12, 31, 23, 59, 59, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # late
                (datetime.datetime(2026, 1, 1, 0, 30, 1, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 datetime.timedelta(minutes=30),
                 datetime.datetime(2026, 1, 1, 0, 30, 1, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                ]

        for a, b, c, expected in cases:
            with self.subTest(a=a, b=b, c=c):
                self.assertEqual(util.check_out_time(a, b, c), expected)

class TestRoundTimeByMinute(unittest.TestCase):

    def test_cases(self):
        cases = [
                # ordinary
                (datetime.datetime(2026, 1, 1, 0, 0, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'up',
                 datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 0, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'down',
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 0, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'round',
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 4, 22, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'round',
                 datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                # edge
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'up',
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'up',
                 datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'down',
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'down',
                 datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 2, 30, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 5,
                 'round',
                 datetime.datetime(2026, 1, 1, 0, 5, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 3,
                 'round',
                 datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                (datetime.datetime(2026, 1, 1, 0, 3, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")),
                 3,
                 'round',
                 datetime.datetime(2026, 1, 1, 0, 3, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York"))),
                ]

        for a, b, c, expected in cases:
            with self.subTest(a=a, b=b, c=c):
                print(a, b, c, expected)
                self.assertEqual(util.round_time_by_minute(a, b, c), expected)

if __name__ == '__main__':
    unittest.main()
