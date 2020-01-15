from src.entity.TenderLanguageEntity import TenderLanguageEntity
import json

class Tender:

    def __init__(self, id, cpvs):
        self.id = id
        self.cpvs = cpvs
        self.lang_entities = {}
    
    def add_language_entity(self, language_key, title, description = ""):
        entity = TenderLanguageEntity(title,description)
        self.lang_entities[language_key] = entity
    
    def get_title(self, language):
        return self.lang_entities[language].title

    def get_description(self, language):
        return self.lang_entities[language].description

    def get_json(self):
        contract = {"id": self.id, "cpvs": self.cpvs}
        lang_list = []
        for k,v in self.lang_entities.items():
            lang_entry = {}
            lang_entry["title"] = v.title
            lang_entry["description"] = v.description
            lang_list.append(lang_entry)
        contract["text"] = lang_list

        return json.dumps(contract)