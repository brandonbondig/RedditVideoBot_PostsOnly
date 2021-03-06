import re
import json


def sanitize_text(text: str) -> str:
    r"""Sanitizes the text for tts.
        What gets removed:
     - following characters`^_~@!&;#:-%“”‘"%*/{}[]()\|<>?=+`
     - any http or https links
     - any swearwords

    Args:
        text (str): Text to be sanitized

    Returns:
        str: Sanitized text
    """

    # remove any urls from the text
    regex_urls = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

    result = re.sub(regex_urls, " ", text)

    # note: not removing apostrophes
    regex_expr = r"\s['|’]|['|’]\s|[\^_~@!&;#:\-%“”‘\"%\*/{}\[\]\(\)\\|<>=+]"
    result = re.sub(regex_expr, " ", result)
    result = result.replace("+", "plus").replace("&", "and")

    # Swapps swearwords from ./blacklisted.json
    blacklisted_result = result
    with open("./blacklisted.json") as json_file:
        data = json.load(json_file)

    for word, replacement in data.items():
        blacklisted_result = re.sub(r'\b' + word + r'\b', replacement, blacklisted_result)

    # remove extra whitespace
    return " ".join(result.split()), " ".join(blacklisted_result.split())
