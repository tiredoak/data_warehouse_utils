import doctest
import os
import subprocess
from collections import Counter

from helpers import *


def repeated_names(list_of_filepaths):
    """
    Given a list of filepaths, returns a list of filenames which are repeated.

    :param list_of_filepaths: list
    :return: list

    >>> repeated_names(["user/123/message_1.json", "user/435/message_1.json", "another/file/new_filename.json"])
    ['message_1.json']

    >>> repeated_names(["user/123/message_1.json", "user/435/message_2.json", "another/file/new_filename.json"])
    []

    >>> repeated_names(["user/123/message_1.json", "user/435/message_2.json", "another/file/message_1.csv"])
    []
    """
    # traverse filenames
    filenames = map(
        lambda filepath: extract_filename(filepath, include_extension=True),
        list_of_filepaths,
    )
    filename_counts = Counter(filenames).most_common()
    repeated_filenames = [_file[0] for _file in filename_counts if _file[1] > 1]
    return repeated_filenames


def get_data_source_files(data_source, file_list, sort=True):
    """
    Given a data source and a list of files, returns just the file pertaining to that data source.

    :param data_source: string
    :param file_list: list
    :param sorted: bool
    :return: list

    >>> get_data_source_files('data_source_1', ['data_source_1/filters_0000.json', 'data_source_2/filters_0000.json'])
    ['data_source_1/filters_0000.json']

    >>> get_data_source_files('data_source_1', ['data_source_1/path/to/file/filters_0000.json', 'data_source_1/filters_0000.json'])
    ['data_source_1/filters_0000.json', 'data_source_1/path/to/file/filters_0000.json']

    >>> get_data_source_files('data_source_2', ['data_source_1/path/to/file/filters_0000.json', 'data_source_1/filters_0000.json'])
    []

    """
    jsons_and_csvs = filter_json_and_csv(file_list)
    results = list(
        filter(lambda _file: os.path.join(data_source, "") in _file, jsons_and_csvs)
    )
    return sorted(results) if sort else results


def get_file_format(data_source, file_list):
    """
    Given a data source and its files, returns the equivalent format to pass in to BigQuery.
    https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table#source_format
    All files need to have the same extension

    :param filename: string
    :return: string

    >>> get_file_format('data_source_1', ['data_source_1/filters_0000.json', 'data_source_2/filters_0000.json'])
    'NEWLINE_DELIMITED_JSON'

    >>> get_file_format('data_source_1', ['data_source_1/filters_0000.csv', 'data_source_1/filters_0000.csv'])
    'CSV'

    >>> get_file_format('data_source_1', ['data_source_1/filters_0000.txt'])
    Traceback (most recent call last):
        ...
    ValueError: Only JSON and CSV files should be uploaded
    """
    # only accept JSON and CSVs for now
    jsons_and_csvs = filter_json_and_csv(file_list)

    data_source_files = get_data_source_files(data_source, jsons_and_csvs, sort=True)

    all_json = all(file.endswith(".json") for file in file_list)
    all_csv = all(file.endswith(".csv") for file in file_list)

    if all_json:
        return "NEWLINE_DELIMITED_JSON"
    elif all_csv:
        return "CSV"
    else:
        raise ValueError("Only JSON and CSV files should be uploaded")


def return_folder_name(filepath):
    """
    Given a filepath, returns the corresponding folder name.

    :param filepath: string
    :return: string
    """
    filename = extract_filename(filepath, include_extension=True)
    return filename_to_folder_name(filename)


def convert_to_newline_delimited_json(filepath, jq_command="jq -c '.[]'"):
    """
    Convert a file to newline delimited JSON with jq

    :param filepath: string
    :return: string
    """
    command = f"{jq_command} {filepath}"
    if not is_ndjson_file(filepath):
        ndjson_bytes = subprocess.check_output(command, shell=True)
        ndjson_str = ndjson_bytes.decode().strip()
        return ndjson_str


if __name__ == "__main__":
    doctest.testmod()
