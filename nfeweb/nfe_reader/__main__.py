import logging

from nfeweb.nfe_reader.models import Nfe
from nfeweb.nfe_reader.nfe import parse_nfes
from nfeweb.nfe_reader.report import console_report, csv_report, sqlite_report

LOGGER = logging.getLogger(__name__)


def main():
    nfes: list[Nfe] = parse_nfes()
    console_report(nfes)
    csv_report(nfes)
    sqlite_report(nfes)


if __name__ == "__main__":
    main()
