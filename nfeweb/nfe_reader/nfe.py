import logging

import requests
from bs4 import BeautifulSoup
from furl import furl

from nfeweb.nfe_reader.models import Config, Nfe
from nfeweb.nfe_reader.parser import parse_nfe

LOGGER = logging.getLogger(__name__)


# def read_config() -> Config:
#     return Config.parse_file("nfe_config.json")


def fetch_nfe_html(endpoint: str, nfe_code: str) -> BeautifulSoup | None:
    LOGGER.info("Fetching NFe '%s'.", nfe_code)
    url = endpoint.format(nfe_code)
    resp = requests.get(url)

    if resp.ok:
        return BeautifulSoup(resp.text, "html.parser")

    LOGGER.error("Unable to fetch NFE with code %s. Response text: %s", nfe_code, resp.text)
    return None


# def parse_nfes():
#     nfes: list[Nfe] = []
#     config: Config = read_config()
#     LOGGER.info("Found %s NFe to fetch.", len(config.nfe_codes))
#
#     for nfe_code in config.nfe_codes:
#         html = fetch_nfe_html(config.nfe_endpoint, nfe_code)
#         nfe = parse_nfe(html)
#         nfes.append(nfe)
#         sorted(nfe)
#
#     return nfes


def parse_nfe_by_url(url: str) -> Nfe:
    nfe_endpoint = "https://www.sefaz.rs.gov.br/ASP/AAE_ROOT/NFE/SAT-WEB-NFE-NFC_QRCODE_1.asp?p={}"
    nfe_code = furl(url).args.get("p")

    html = fetch_nfe_html(nfe_endpoint, nfe_code)
    nfe = parse_nfe(html)
    return nfe
