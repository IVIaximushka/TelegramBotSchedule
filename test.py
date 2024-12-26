import unittest

import pandas as pd

from services.parsing_tools import (_add_hours, _filter_exams,
                                    _filter_semester, _filter_tests)


class TestVector(unittest.TestCase):
    # Создание контекста
    def setUp(self):
        self.data_frame = pd.DataFrame(
            data=[
                [
                    1,
                    "математика",
                    "360",
                    "144",
                    "72",
                    "0",
                    "72",
                    "198",
                    "0",
                    "36",
                    "0",
                    "36",
                    None,
                    "+",
                    "36",
                    "0",
                    "36",
                    "+",
                    None,
                ],
                [
                    2,
                    "информатика",
                    "360",
                    "144",
                    "72",
                    "0",
                    "72",
                    "198",
                    "0",
                    None,
                    None,
                    None,
                    None,
                    None,
                    "72",
                    "0",
                    "72",
                    None,
                    "+",
                ],
                [
                    3,
                    "алгебра",
                    "360",
                    "144",
                    "72",
                    "0",
                    "72",
                    "198",
                    "0",
                    "72",
                    "0",
                    "72",
                    "+",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            columns=[
                "id",
                "name",
                "all",
                "all_aud",
                "all_lec",
                "all_prac",
                "all_lab",
                "indep",
                "control",
                "first_lec",
                "first_prac",
                "first_lab",
                "first_ex",
                "first_test",
                "second_lec",
                "second_prac",
                "second_lab",
                "second_ex",
                "second_test",
            ],
        )

    # Удаление данных
    def tearDown(self):
        del self.data_frame

    def test_filter_semester(self):
        data = _filter_semester(self.data_frame, 1)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][2], "алгебра")
        data = _filter_semester(self.data_frame, 2)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")
        data = _filter_semester(self.data_frame, 0)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")
        self.assertEqual(data["name"][2], "алгебра")

    def test_filter_exams_true(self):
        data = _filter_exams(self.data_frame, 1, True)
        self.assertEqual(len(data), 1)
        self.assertEqual(data["name"][2], "алгебра")
        data = _filter_exams(self.data_frame, 2, True)
        self.assertEqual(len(data), 1)
        self.assertEqual(data["name"][0], "математика")
        data = _filter_exams(self.data_frame, 0, True)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][2], "алгебра")

    def test_filter_exams_false(self):
        data = _filter_exams(self.data_frame, 1, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")
        data = _filter_exams(self.data_frame, 2, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][1], "информатика")
        self.assertEqual(data["name"][2], "алгебра")
        data = _filter_exams(self.data_frame, 0, False)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")
        self.assertEqual(data["name"][2], "алгебра")

    def test_filter_tests_true(self):
        data = _filter_tests(self.data_frame, 1, True)
        self.assertEqual(len(data), 1)
        self.assertEqual(data["name"][0], "математика")
        data = _filter_tests(self.data_frame, 2, True)
        self.assertEqual(len(data), 1)
        self.assertEqual(data["name"][1], "информатика")
        data = _filter_tests(self.data_frame, 0, True)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")

    def test_filter_tests_false(self):
        data = _filter_tests(self.data_frame, 1, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][1], "информатика")
        self.assertEqual(data["name"][2], "алгебра")
        data = _filter_tests(self.data_frame, 2, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][2], "алгебра")
        data = _filter_tests(self.data_frame, 0, False)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["name"][0], "математика")
        self.assertEqual(data["name"][1], "информатика")
        self.assertEqual(data["name"][2], "алгебра")

    def test_filter_hours_true(self):
        data = _add_hours(_filter_semester(self.data_frame, 1), 1, True)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["hours"][0], "математика: 36/0/36")
        self.assertEqual(data["hours"][2], "алгебра: 72/0/72")
        data = _add_hours(_filter_semester(self.data_frame, 2), 2, True)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["hours"][0], "математика: 36/0/36")
        self.assertEqual(data["hours"][1], "информатика: 72/0/72")
        data = _add_hours(_filter_semester(self.data_frame, 0), 0, True)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["hours"][0], "математика: 72/0/72")
        self.assertEqual(data["hours"][1], "информатика: 72/0/72")
        self.assertEqual(data["hours"][2], "алгебра: 72/0/72")

    def test_filter_hours_false(self):
        data = _add_hours(_filter_semester(self.data_frame, 1), 1, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["hours"][0], "математика")
        self.assertEqual(data["hours"][2], "алгебра")
        data = _add_hours(_filter_semester(self.data_frame, 2), 2, False)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["hours"][0], "математика")
        self.assertEqual(data["hours"][1], "информатика")
        data = _add_hours(_filter_semester(self.data_frame, 0), 0, False)
        self.assertEqual(len(data), 3)
        self.assertEqual(data["hours"][0], "математика")
        self.assertEqual(data["hours"][1], "информатика")
        self.assertEqual(data["hours"][2], "алгебра")


if __name__ == "__main__":
    unittest.main()
