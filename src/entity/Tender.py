from entity.TenderLanguageEntity import TenderLanguageEntity

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
