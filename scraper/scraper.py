import requests
from bs4 import BeautifulSoup
import logging
import json
from mjx_data import ALLOWED_MATHJAX_TAGS

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


def serializer(latex: str) -> str:
    """
    Serialize the given latex string.

    :param latex: The latex string.

    :return: The serialized string.
    """
    serialized_string = json.dumps(latex)
    return serialized_string


def write_to_file(content: list | set, file_name: str) -> None:
    """
    Write the contents to a file.

    :param content: The attribute contents.

    :return: Nothing.
    """

    f_mode = "a"
    with open(file=file_name, mode=f_mode) as file:
        for item in set(content):
            file.write(item + "\n")


def attr_scraper(content: str):
    """
    Scrape the attributes from the html content.

    :param content: The HTML mathjax content.

    :return: The mathjax attributes.
    """

    soup = BeautifulSoup(content, "html.parser")

    elements: list = soup.find_all()
    attrs_dump: list = []
    for element in elements:
        attributes = element.attrs
        if attributes:
            for attribute, value in attributes.items():
                attrs_dump.append(attribute)
    return attrs_dump


def tag_scraper(content: str):
    """
    Scrape the tags fro the html content.

    :param content: The HTML mathjax content.

    :return: The mathjax tags.
    """
    soup = BeautifulSoup(content, "html.parser")

    elements: list = soup.find_all()
    tag_dump: list = []
    for tag in elements:
        if tag.name not in ALLOWED_MATHJAX_TAGS:
            tag_dump.append(tag.name)
    return tag_dump


def make_req(latex: str, url: str, file_name: str, scrape_tags: bool) -> str:
    """
    Request the node service to return mathjax.

    :param latex: The latex string.
    :param method: The scraping method

    :return: The mathjax HTML string.
    """
    payload = json.dumps({"latexString": latex})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        if scrape_tags:
            res = tag_scraper(content=response.text)
        res = attr_scraper(content=response.text)
        write_to_file(content=res, file_name=file_name)
    else:
        LOGGER.debug(
            f"Failed to retrieve the webpage. Status code: {response.status_code}"
        )


def driver(url: str, file_name: str) -> None:
    """
    The driver function for scraping the tags or attributes.
    """

    with open(file=file_name, mode="r") as file:
        for line in file:
            print(line)
            make_req(
                latex=serializer(latex=line),
                url=url,
                scrape_tags=True,
                file_name="mjx-tags.txt",
            )


if __name__ == "__main__":

    #: The Node migration tool's URL.

    driver(
        url="http://localhost:3000/api/convert-latex",
        file_name="ltx-ktx-supported-funcs.tex",  # The input file path/name
    )
