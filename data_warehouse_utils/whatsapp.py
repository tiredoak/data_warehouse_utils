import doctest
import os
import re

from data_warehouse_utils.helpers import clean_filename, replace_diacritics


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


def pre_process_whatsapp_filename(gcs_raw_filepath):
    """
    Given a raw filepath in GCS for a WhatsApp chat, return the pre_processed filename

    :param gcs_raw_filepath: string
    :return: string

    >>> pre_process_whatsapp_filename("whatsapp/chats/WhatsApp Chat - Gonçalo Miranda/_chat.txt")
    'whatsapp/chats/goncalo_miranda/chat.json'

    >>> pre_process_whatsapp_filename("whatsapp/chats/WhatsApp Chat - António Bênção/_chat.txt")
    'whatsapp/chats/antonio_bencao/chat.json'

    >>> pre_process_whatsapp_filename("whatsapp/chats/WhatsApp Chat - 🐮/_chat.txt")
    'whatsapp/chats/🐮/chat.json'
    """
    pattern = r"whatsapp\/chats\/WhatsApp\WChat\W-\W(.*)\/_(chat)\.txt"
    matches = re.match(pattern, gcs_raw_filepath)
    entity = matches.group(1)
    filename = matches.group(2)

    entity = replace_diacritics(entity)
    entity = clean_filename(entity.lower())
    return os.path.join("whatsapp", "chats", entity, filename + ".json")


if __name__ == "__main__":
    doctest.testmod()
