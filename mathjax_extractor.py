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


if __name__ == "__main__":
    # /home/nova/work/InstaQP-MVP/mathjax-tags/data/mjx-data-1.html

    base_path: str = "/home/nova/work/InstaQP-MVP/mathjax-tags"
    dir_path: str = "data"
    file_name: str = "mjx-data-1.html"

    # base_path: str = "/home/nova/work/MathJax-src/ts/"
    # dir_path: str = "output/chtml/Wrappers/"
    # file_name: str = "maction.ts"

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

    print(f"{total_extracted_tags=}")
    print(f"{total_ext_tags_rm_dups=}")

    now = datetime.now()
    LOGGER.info("Writing the data to a text file... %s", now)

    output_file = f"extracted_data-{now}.txt"
    with open(file=output_file, mode="w") as file:
        for item in set(results):
            file.write(item + "\n")
