import requests
from bs4 import BeautifulSoup
import logging
import json


LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


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
            LOGGER.debug(f"Element Name: {element.name}")
            for attribute, value in attributes.items():
                attrs_dump.append(attribute)
    return attrs_dump


def make_req(latex: str, url: str) -> str:
    """
    Request the node service to return mathjax.

    :param latex: The latex string.

    :return: The mathjax HTML string.
    """
    payload = json.dumps({"latexString": latex})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        res = attr_scraper(content=response.text)
        print(set(res))
    else:
        LOGGER.debug(
            f"Failed to retrieve the webpage. Status code: {response.status_code}"
        )


if __name__ == "__main__":
    latex_data = """"""
    make_req(latex=latex_data, url="http://localhost:3000/api/convert-latex")
