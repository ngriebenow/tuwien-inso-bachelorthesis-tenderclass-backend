import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import re

class TedExtractor:

    def extract(self, xml_doc, language):

        # parse document id
        ted_export = xml_doc.findAll(re.compile("TED_EXPORT"))[0]
        tender_id = "EU" + ted_export['DOC_ID']

        # parse cpv code
        try:
            tender_cpvs = []
            cpv_codes = xml_doc.findAll(re.compile("(CPV_CODE)|(ORIGINAL_CPV)"))
            for cpv_code in cpv_codes:
                try:
                    tender_cpvs.append(cpv_code["CODE"])
                except:
                    pass
            contract["cpv"] = cpvs
        except:
            logger.error("Could not retrieve CPV for contract")
            logger.error(xml_doc.prettify())
            raise Exception("could not retrieve CPV for contract")


        tender = Tender(tender_id, tender_cpvs)


        # extract title and description for each language
        for lg in lang:
            
            title = None
            short_desc = None

            try:
                ml_titles_section = xml_doc.findAll(re.compile("ML_TITLES"))
                if ml_titles_section:
                    ml_ti_doc = ml_titles_section[0].findAll(re.compile("ML_TI_DOC"),{"LG": lg})
                    if ml_ti_doc:
                        ti_text = ml_ti_doc[0].findAll(re.compile("TI_TEXT"))[0]
                        title = extract_text(ti_text)
            except:
                logger.error(f"Error while parsing title at contract {doc_id}")
            
            try:
                f02_2014 = xml_doc.findAll(re.compile(r'F[0-9][0-9]_2014'), {"LG": lg})
                if f02_2014:
                    f02_2014 = f02_2014[0]

                    object_contract = f02_2014.findAll(re.compile('OBJECT_CONTRACT'))
                    if object_contract:
                        object_contract = object_contract[0]

                        if not title:
                            title = extract_text(object_contract.findAll(re.compile('TITLE'))[0])
                        if not short_desc:
                            short_desc = extract_text(object_contract.findAll(re.compile('SHORT_DESC'))[0])
            except:
                logger.error(f"Could not pass Fxx_2014 document")  

            try:
                f02_2014 = xml_doc.findAll(re.compile("CONTRACT"), {"LG": lg})
                if f02_2014:
                    f02_2014 = f02_2014[0]

                    object_contract = f02_2014.findAll(re.compile('OBJECT_CONTRACT'))
                    if object_contract:
                        object_contract = object_contract[0]

                        if not title:
                            title = extract_text(object_contract.findAll(re.compile('TITLE_CONTRACT'))[0])
                        if not short_desc:
                            short_desc = extract_text(object_contract.findAll(re.compile('SHORT_CONTRACT_DESCRIPTION'))[0])
            except:
                logger.error(f"Could not pass CONTRACT document")

            tender.add_language_entity(lg, title, short_descr)

        return tender