import os
import unittest
from unittest import TestCase
from typing import Tuple

import main


class Test(TestCase):
    def __init__(self, method_name: str):
        super().__init__(method_name)
        self._json_files: Tuple[str, str] = ("test_main_1.json", "test_main_2.json")
        self._csv_file: str = "test_main.csv"

    def test_validate_json(self):
        valid = {"student1": ["view_grades", "view_classes"],
                 "student2": ["view_grades", "view_classes"],
                 "teacher": ["view_grades", "change_grades", "add_grades", "delete_grades", "view_classes"]}
        invalid = [{"student1": ["view_grades", "view_classes"]},
                   {"student2": ["view_grades", "view_classes"]},
                   {"teacher": ["view_grades", "change_grades", "add_grades", "delete_grades", "view_classes"]}]
        self.assertTrue(main.validate_json(valid))
        self.assertFalse(main.validate_json(invalid))

    def test_parse_json(self):
        result_one = main.parse_json(self._json_files[0])
        result_two = main.parse_json(self._json_files[1])
        self.assertListEqual(["student1", "student2", "student3", "teacher"], list(result_one.keys()))
        self.assertListEqual(["view_grades", "change_grades", "add_grades", "delete_grades", "view_classes"],
                             result_one["teacher"])
        self.assertListEqual(["student1", "student2", "teacher", "principle"], list(result_two.keys()))
        self.assertListEqual(["view_grades", "view_classes", "change_classes", "add_classes", "delete_classes"],
                             result_two["principle"])

    def test_update_lists_to_sets(self):
        records = {"student1": ["view_grades", "view_classes"]}
        result = next(main.update_lists_to_sets(records))
        self.assertEqual("student1", result[0])
        self.assertTrue("view_grades" in result[1])

    def test_create_csv(self):
        try:
            headers = ['a', 'b', 'c']
            result = main.create_csv(self._csv_file, headers)
            self.assertTrue(result)
            with open(self._csv_file, 'r') as fp:
                self.assertEqual("a,b,c\n", fp.read())
        finally:
            if main.os.path.exists(self._csv_file):
                main.os.remove(self._csv_file)

    def test_write_to_csv(self):
        try:
            headers = ["person", "view_grades", "change_grades", "add_grades",
                       "delete_grades", "view_classes", "change_classes", "add_classes",
                       "delete_classes"]
            records = {"student1": ["view_grades", "view_classes"],
                       "student2": ["view_grades", "view_classes"],
                       "teacher": ["view_grades", "change_grades", "add_grades", "delete_grades", "view_classes"]}
            result = main.write_to_csv(self._csv_file, headers, records)
            self.assertTrue(result)
            with open(self._csv_file, 'r') as fp:
                self.assertEqual("person,view_grades,change_grades,add_grades,"
                                 "delete_grades,view_classes,change_classes,add_classes,"
                                 "delete_classes\nstudent1,0,1,0,0,0,1,0,0,0\n"
                                 "student2,0,1,0,0,0,1,0,0,0\nteacher,0,1,1,1,1,1,0,0,0\n", fp.read())
        finally:
            if main.os.path.exists(self._csv_file):
                main.os.remove(self._csv_file)

    def test_main(self):
        try:
            self.assertEqual(1, main.main(["main.py"]))
            self.assertEqual(1, main.main(["main.py", self._json_files[0]]))
            self.assertEqual(0, main.main(["main.py", self._json_files[0], self._csv_file]))
            with open(self._csv_file, 'r') as fp:
                self.assertEqual("person,view_grades,change_grades,add_grades,"
                                 "delete_grades,view_classes,change_classes,add_classes,"
                                 "delete_classes\nstudent1,0,1,0,0,0,1,0,0,0\n"
                                 "student2,0,1,0,0,0,1,0,0,0\nstudent3,0,1,0,0,0,1,0,0,0\n"
                                 "teacher,0,1,1,1,1,1,0,0,0\n", fp.read())
        finally:
            if main.os.path.exists(self._csv_file):
                main.os.remove(self._csv_file)


if __name__ == '__main__':
    unittest.main()
