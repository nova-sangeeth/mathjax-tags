"""
Mathjax tag and attribute extractor
======================================
This program is used to extract all the HTML tags from mathjax's  source code.
"""
import re
import os
from pathlib import Path
import logging
from datetime import datetime

# initialize the logger
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_time() -> datetime:
    """
    Get the current time.

    :return: The date and time stamp string.
    """

    return datetime.now()


def extract_mjx_tags(file_path: str):
    try:
        with open(file_path, "r") as file:
            text = file.read()

            # Use regular expression to find words starting with "mjx"
            mjx_words = re.findall(r"\bmjx-\w*\b", text, re.IGNORECASE)

            return mjx_words
    except FileNotFoundError:
        LOGGER.debug(f"The file '{file_path}' was not found.")
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")


def mjx_data_writer(base_path: str, dir_path: str) -> None:
    """
    Function to write the mjx tags to a file.

    :param base_path: The base path for the directory.
    :param dir_path: The dir_path for the directory.

    :return: Nothing.
    """

    # Construct the file path
    directory_path: str = os.path.join(base_path, dir_path)

    # List the files in the given directory
    results: list = []

    for file_path in Path(directory_path).iterdir():
        LOGGER.debug(f"The file path: {file_path} ")
        mjx_words = extract_mjx_tags(file_path=file_path)

        if mjx_words:
            LOGGER.debug(f"Words starting with 'mjx' in the file: {file_path}")
            for word in mjx_words:
                results.append(word)
        else:
            LOGGER.error(
                f"No words starting with 'mjx' were found in the file: {file_path}"
            )
    # Get the len of the results
    total_extracted_tags = len(results)
    total_ext_tags_rm_dups = len(set(results))

    LOGGER.info(f"{total_extracted_tags=}")
    LOGGER.info(f"{total_ext_tags_rm_dups=}")

    # Get the time
    now = get_time()

    LOGGER.info("Writing the data to a text file... %s", now)

    output_file = f"extracted_data-{now}.txt"
    with open(file=output_file, mode="w") as file:
        for item in set(results):
            file.write(item + "\n")


if __name__ == "__main__":

    base_path: str = "/home/nova/work/MathJax-src/"
    dir_path: str = "output/chtml/Wrappers/"
    file_name: str = "maction.ts"

    # mjx_data_writer(base_path=base_path, dir_path=dir_path)
