from typing import List

from entity.Tender import Tender
from fetcher.ted.TedDownloader import TedDownloader
from fetcher.ted.TedExtractor import TedExtractor
class TedFetcher:

    def __init__(self):
        self.ted_downloader = TedDownloader()
        self.ted_extractor = TedExtractor()

    MAX_PAGE_COUNT = 100

    def get(self, count : int, load_documents : bool = False, search_criteria : str = "", languages : List[str] = ["DE"], page_offset : int = 0) -> List[Tender]:

        ted_docs = []
        page = 1
        last_docs_count = -1

        while last_docs_count != len(ted_docs):
            last_docs_count = len(ted_docs)

            xml_docs = self.ted_downloader.get_xml_contracts(page,MAX_PAGE_COUNT, search_criteria, page_offset=page_offset)

            for xml_doc in xml_docs:
                if (xml_doc != None):

                    doc = self.ted_extractor.extract(xml_doc, lang)

                    if (doc != None):

                        documents = []
                        if (load_documents):

                            doc_links = self.ted_extractor.extract_doc_links(xml_doc)
                            logger.info("found doc links: " + str(doc_links))

                            for doc_link in doc_links:
                                documents.append(doc_parse.get_doc_content(doc_link))

                            # TODO add document links to tender

                        ted_docs.append(doc)

                        if (len(ted_docs) == count):
                            return ted_docs
            page += 1
        
        return ted_docs
