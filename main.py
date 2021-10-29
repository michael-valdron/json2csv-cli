import csv
import json
import os.path
import sys
from typing import List, Dict, Any, Optional, Set, Iterator, Tuple


def validate_json(json_input: Any) -> bool:
    """
    Validates the form of the parsed JSON input. When the form is valid return `True` else return `False`.

    :type json_input: Any
    :rtype: bool
    :param json_input: JSON object to validate.
    :returns: Boolean which indicates whether form is valid.
    """
    return type(json_input) == dict and \
        all(type(k) == str and type(v) == list and all(type(vi) == str for vi in v) for k, v in json_input.items())


def parse_json(path: str) -> Optional[Dict[str, List[str]]]:
    """
    Parses JSON file into python object. Returns parsed entity if successful. If error occurs or form is invalid prints
    issue to console and returns `None`.

    :type path: str
    :rtype: Optional[Dict[str, List[str]]]
    :param path: Directory path to JSON file to parse.
    :returns: Parsed JSON object in proper form, or None if error occurs or source JSON is an invalid form.
    """
    try:
        with open(path, 'r') as fp:
            json_input = json.load(fp)
            if validate_json(json_input):
                return json_input
            else:
                print(("JSON structure is invalid, should be in the form of\n" +
                       "{\"student1\": [\n"
                       "        \"view_grades\",\n"
                       "        ...\n"
                       "    ]\n"
                       "...\n"
                       "}\n"
                       "but is\n") + f"{json.dumps(json_input)}")
                return None
    except json.decoder.JSONDecodeError as e:
        print(str(e))
        return None


def update_lists_to_sets(parsed_json: Dict[str, List[str]]) -> Iterator[Tuple[str, Set[str]]]:
    """
    Creates iterator of key / value pairs where the new values are converted sets of the old values (lists).

    :type parsed_json: Dict[str, List[str]]
    :rtype: Iterator[Tuple[str, Set[str]]]
    :param parsed_json: Parsed JSON entity to convert to key / set(value) iterator.
    :returns: Iterator of key / set(value) pairs.
    """
    for k, v in parsed_json.items():
        yield k, set(v)


def create_csv(out_file: str, fieldnames: List[str], delimiter: str = ',', quotechar: str = '"') -> bool:
    """
    Creates CSV file and writes fieldnames at the top. Returns `True` if successful else prints error to the console
    and returns `False`.

    :type out_file: str
    :type fieldnames: List[str]
    :type delimiter: str
    :type quotechar: str
    :rtype: bool
    :param out_file: New CSV file path.
    :param fieldnames: List of fieldnames to use in CSV.
    :param delimiter: Delimiter to use in CSV file.
    :param quotechar: Quote character to wrap cells.
    :return: Returns boolean of whether writing to CSV was successful or not.
    """
    try:
        with open(out_file, 'x', newline='') as fp:
            csv.writer(fp, delimiter=delimiter, quotechar=quotechar).writerow(fieldnames)
        return True
    except IOError as e:
        print(str(e))
        return False


def write_to_csv(out_file: str, fieldnames: List[str], parsed_json: Dict[str, List[str]],
                 delimiter: str = ',', quotechar: str = '"', overwrite: bool = True) -> bool:
    """
    Writes parsed JSON entity to CSV records within a specified CSV file.

    :type out_file: str
    :type fieldnames: List[str]
    :type parsed_json: Dict[str, List[str]]
    :type delimiter: str
    :type quotechar: str
    :type overwrite: bool
    :rtype: bool
    :param out_file: CSV file path.
    :param fieldnames: List of fieldnames to use in CSV.
    :param parsed_json: Parsed JSON entity to write to CSV file.
    :param delimiter: Delimiter to use in CSV file.
    :param quotechar: Quote character to wrap cells.
    :param overwrite: True (default): Overwrites file if exists. False: Appends to file if exists.
    :return: Returns boolean of whether writing to CSV was successful or not.
    """
    if overwrite and os.path.exists(out_file):
        os.remove(out_file)
    if not os.path.exists(out_file) and not create_csv(out_file, fieldnames, delimiter, quotechar):
        return False

    try:
        with open(out_file, 'a', newline='') as fp:
            writer = csv.writer(fp, delimiter=delimiter, quotechar=quotechar)
            for k, v in update_lists_to_sets(parsed_json):
                writer.writerow((k, *map(lambda field: int(field in v), fieldnames[1:])))
        return True
    except IOError as e:
        print(str(e))
        return False


def main(args: List[str]) -> int:
    """
    Main entry to commandline tool.

    **CLI Usage**

    usage: python main.py <input>.json <output>.csv

    example: python main.py in.json out.csv


    **Exit Status Codes**

    0 - Exits successfully.

    1 - Exits due to missing or too many arguments.

    2 - Exits to JSON read error.

    3 -Exits to CSV write error.

    :param args: Arguments given in CLI.
    :return: Exit status code.
    """
    if len(args) != 3:
        print("""
        usage: python main.py <input>.json <output>.csv
        example: python main.py in.json out.csv
        """)
        return 1
    in_file, out_file = args[1:]
    parsed_json = parse_json(in_file)
    headers = ["person", "view_grades", "change_grades", "add_grades",
               "delete_grades", "view_classes", "change_classes", "add_classes",
               "delete_classes"]

    if parsed_json is None:
        print("Errors when reading JSON file.")
        return 2
    elif not write_to_csv(out_file, headers, parsed_json):
        print("Errors when writing to CSV file.")
        return 3

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
