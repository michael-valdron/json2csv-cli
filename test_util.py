import csv
import json
import os.path
import unittest


class Test(unittest.TestCase):
    def __init__(self, method_name: str):
        super().__init__(method_name)
        self._json_file: str = "test_main_1.json"
        self._csv_file: str = "test_util.csv"

    def test_json_load(self):
        expected = {"student1": ["view_grades", "view_classes"],
                    "student2": ["view_grades", "view_classes"],
                    "student3": ["view_grades", "view_classes"],
                    "teacher": ["view_grades", "change_grades", "add_grades", "delete_grades", "view_classes"]}
        with open(self._json_file, 'r') as fp:
            self.assertEqual(expected, json.load(fp))

    def test_json_dumps(self):
        records = {"student1": ["view_grades", "view_classes"]}
        self.assertEqual("{\"student1\": [\"view_grades\", \"view_classes\"]}", json.dumps(records))

    def test_csv_write(self):
        try:
            with open(self._csv_file, 'x') as fp:
                csvwriter = csv.writer(fp, delimiter=',', quotechar='"')
                csvwriter.writerow((1, 2, 3))
            with open(self._csv_file, 'r') as fp:
                self.assertEqual("1,2,3\n", fp.read())
        finally:
            if os.path.exists(self._csv_file):
                os.remove(self._csv_file)


if __name__ == '__main__':
    unittest.main()
