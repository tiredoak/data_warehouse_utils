import doctest
import json
import re

input = "data_warehouse_utils/_chat.txt"
output = "data_warehouse_utils/chat_output.json"


def is_complete_message(s):
    """
    Given a WhatsApp chat exported string, returns if string is a complete message

    :param s: string
    :return: bool

    >>> is_complete_message("[2021-05-05, 11:44:26] A: message content")
    True

    >>> is_complete_message("Message content")
    False
    """
    pattern = r"^\[\d{4}-\d{2}-\d{2},\W\d{2}:\d{2}:\d{2}]"
    results = re.search(pattern, s)
    return True if results else False


def count_messages(filepath):
    """
    Given a WhatsApp chat txt export, returns the number of messages exchanged.

    :param filepath: string
    :return: int
    """
    total_messages = 0
    pattern = r"\[\d{4}-\d{2}-\d{2},\s\d{2}:\d{2}:\d{2}\]"

    with open(filepath) as f:
        for line in f:
            matches = re.findall(pattern, line)
            total_messages += len(matches)
    return total_messages


def parse_message(s):
    """
    Given a WhatsApp chat string, returns the message as a dict.

    :param s: string
    :return: dict

    >>> parse_message("[2021-01-01, 00:00:00] Author: Message")
    {'timestamp': '2021-01-01 00:00:00', 'author': 'Author', 'content': 'Message'}
    """
    pattern = r"\[(\d{4}-\d{2}-\d{2}),(\W\d{2}:\d{2}:\d{2})]\W(.*):\W(.*)"
    # Use regex to extract the timestamp, author, and content from the input string
    match = re.match(pattern, s)
    timestamp = match.group(1) + match.group(2)
    author = match.group(3)
    content = match.group(4)
    # Create a dictionary with the extracted data
    return {"timestamp": timestamp, "author": author, "content": content}


def last_processed_message(filepath):
    with open(filepath, "r") as f:
        # Use seek() to move the file pointer to the end of the file
        f.seek(0, 2)
        # Use tell() to get the current position of the file pointer
        pos = f.tell()
        # Start reading the file backwards, one character at a time
        # until we find the last newline character
        while pos > 0:
            pos -= 1
            f.seek(pos, 0)
            if f.read(1) == "\n":
                break
        # Use readline() to read the last line of the file
        last_line = f.readline().strip()

    return json.loads(last_line)


if __name__ == "__main__":
    print(count_messages(input))
    data = last_processed_message(output)
    print(data["content"])

    new_message = {
        "timestamp": "2021-05-05 11:49:35",
        "author": "Miguel",
        "content": "New last message",
    }

    doctest.testmod()
