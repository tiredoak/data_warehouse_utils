import doctest
import json
import os
import re
from pathlib import Path


def camel_to_snake_case(s):
    """
    Given a string, returns its equivalent as snake case.

    :param s: string
    :return: string

    >>> camel_to_snake_case("CacheRealmReport_Hourly_0.json")
    'cache_realm_report__hourly_0.json'

    >>> camel_to_snake_case("filters_0000.json")
    'filters_0000.json'

    >>> camel_to_snake_case("HowWeFeelEmotions.csv")
    'how_we_feel_emotions.csv'
    """
    s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def clean_filename(filename):
    """
    Given a filename, returns the clean version of that filename.

    :param filename: string
    :return: string

    >>> clean_filename("information_you've_submitted_to_advertisers.json")
    'information_youve_submitted_to_advertisers.json'

    >>> clean_filename("")
    ''

    >>> clean_filename("ContinuumSectionResponseV1_0.json")
    'ContinuumSectionResponseV1_0.json'
    """
    no_spaces = str(filename).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", no_spaces)


def extract_filename(filepath, include_extension=False):
    """
    Given a filepath, extracts just the filename

    :param filepath: string
    :return: string

    >>> extract_filename("user/123/message_1.json")
    'message_1'

    >>> extract_filename("user/123/message_1.json", include_extension=True)
    'message_1.json'

    >>> extract_filename("another/file/new_filename.json")
    'new_filename'

    >>> extract_filename("HowWeFeelEmotions.csv")
    'HowWeFeelEmotions'
    """
    return Path(filepath).stem if not include_extension else os.path.basename(filepath)


def get_top_level_dirs(dir_path):
    """
    Given a dir, returns its top-level dirs.

    :param dir_path: string
    :return: list
    """
    return next(os.walk(dir_path))[1]


def filename_to_folder_name(filename):
    """
    Given a filename, return its corresponding folder name

    :param filename: string
    :return: string

    >>> filename_to_folder_name("CacheRealmReport_Hourly_0.json")
    'cache_realm_report__hourly'

    >>> filename_to_folder_name("filters_0000.json")
    'filters'

    >>> filename_to_folder_name("HowWeFeelEmotions.csv")
    'how_we_feel_emotions'

    >>> filename_to_folder_name("A11yFeatureUsage.json")
    'a11y_feature_usage'

    >>> filename_to_folder_name("ContinuumSectionResponseV1_0.json")
    'continuum_section_response_v1'

    >>> filename_to_folder_name("StreamingHistory1.json")
    'streaming_history'
    """
    snake_case = camel_to_snake_case(filename)
    sanitized = clean_filename(snake_case)

    if filename == ".DS_Store":
        return ""

    pattern = r"(^[a-zA-Z_0-9-]*[a-zA-Z]\d*)(?=_*\d*\.(?:csv|json))"
    match = re.match(pattern, sanitized).group(1)

    # clean files like streaming_history0
    if match[-1].isdigit() and match[-2] != "v":
        return match[0:-1]

    return match


def create_unique_filename(filepath):
    """
    Given a filepath, appends previous part of the path to the filename to make the filename unique.

    :param filepath: string
    :return: string

    >>> create_unique_filename('/path/to/file/pull_request_reviews_000001.json')
    'pull_request_reviews/pull_request_reviews_000001-file.json'

    >>> create_unique_filename("path/filters_0000.json")
    'filters/filters_0000-path.json'

    >>> create_unique_filename("todoist/todoist-filters_0000.json")
    'todoist-filters/todoist-filters_0000-todoist.json'
    """
    dirname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    folder_name = filename_to_folder_name(filename)

    # Check if the filename already contains the dirname
    if name.endswith("-" + os.path.basename(dirname)):
        return filepath

    # Append the dirname to the filename to make it unique
    new_name = f"{name}-{os.path.basename(dirname)}"
    new_filename = f"{new_name}{ext}"
    new_filepath = os.path.join(folder_name, new_filename)

    return new_filepath


def get_file_extension(filename):
    """
    Given a filename/filepath, returns the file extension without the '.'.

    :param filename: string
    :return: string

    >>> get_file_extension("CacheRealmReport_Hourly_0.json")
    'json'

    >>> get_file_extension("filters_0000.csv")
    'csv'

    >>> get_file_extension("filters_0000.txt")
    'txt'
    """
    return os.path.splitext(filename)[1][1:]


def absolute_file_paths(directory):
    """
    Returns a generator of all files under a certain directory.

    :param directory: string
    :return: generator
    """
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def filter_json_and_csv(file_list):
    """
    Given a list of files, returns just the jsons and csv

    :param file_list: list
    :return: list

    >>> filter_json_and_csv(["CacheRealmReport_Hourly_0.json"])
    ['CacheRealmReport_Hourly_0.json']

    >>> filter_json_and_csv(["CacheRealmReport_Hourly_0.json", "something.txt"])
    ['CacheRealmReport_Hourly_0.json']

    >>> filter_json_and_csv(["HowWeFeelEmotions.csv"])
    ['HowWeFeelEmotions.csv']

    >>> filter_json_and_csv(["CacheRealmReport_Hourly_0.txt", "something.txt"])
    []
    """
    return list(filter(lambda f: bool(re.search("(.json|.csv)", f)), file_list))


def is_ndjson_file(filepath):
    """
    Given a filepath, determines if that file is a valid newline-delimited JSON.

    :param filepath: string
    :return: bool
    """
    with open(filepath, "r") as f:
        for line in f:
            try:
                json.loads(line)
            except ValueError:
                return False
    return True


if __name__ == "__main__":
    doctest.testmod()
