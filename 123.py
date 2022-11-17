import os
from pathlib import Path

from dotenv import load_dotenv

from contextlib import contextmanager
from typing import Optional

import xmlschema  # type: ignore
from zeep import Client  # type: ignore
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from settings import ENDPOINT, locate_schema_file

load_dotenv(dotenv_path=Path(".") / "interfax.env")
login = os.getenv("INTERFAX_LOGIN")
password = os.getenv("INTERFAX_PASSWORD")

ENDPOINT = "http://sparkgatetest.interfax.ru/iFaxWebService/iFaxWebService.asmx?WSDL"


def locate_schema_file(filename: str):
    return str(Path(".") / "schemas" / filename)



wdsl_url=ENDPOINT
client = Client(wdsl_url)
client.service.Authmethod(login, password)

wdsl_url=ENDPOINT
session = Session()
session.auth = HTTPBasicAuth(login, password)

client = Client(wdsl_url, transport=Transport(session=session))
xml = client.service.GetCompanyShortReport(210).xmlData
data = get_schema('ShortReport.xsd').to_dict(xml)

c = get_client(login, password)
