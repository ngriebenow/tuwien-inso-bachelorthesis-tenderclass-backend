import base64
import lxml
from bs4 import BeautifulSoup as Soup
import re
import requests
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TedDownloader:
    
    TED_URL_SEARCH = "https://ted.europa.eu/api/v2.0/notices/search"

    def get_xml_contracts(self, page : int, count : int, search_criteria = "" : str, page_offset = 0 : int) -> List[Soup]:

        #TD=[\"Contract notice\"] AND CY=[UK]
        querystring = {"fields":"CONTENT", "pageNum":str(page + page_offset),"pageSize":str(count),"q":"TD=[\"Contract notice\"]" + search_criteria, "reverseOrder":"false","scope":"3","sortField":"ND"}

        response = requests.request("GET", TED_URL_SEARCH, params=querystring)

        logger.info("response with status code " + str(response.status_code))
        if response.status_code != 200:
            logger.error(response.text)

        contracts = []
        for i in range(count):
            try:
                resp_dec = base64.b64decode(response.json()["results"][i]["content"]).decode("utf-8")
                soup = Soup(resp_dec, "xml")
                contracts.append(soup)
            except:
                pass
        
        logger.info("page " + str(page) + " successflly fetched ")
        return contracts