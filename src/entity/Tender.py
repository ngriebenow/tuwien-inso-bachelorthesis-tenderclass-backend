from src.entity.TenderLanguageEntity import TenderLanguageEntity


class Tender:
    """
    This class serves as entity for one tender. It holds the id, the CPV codes and a number of language entities,
    where each of which is a collection of title and description in a certain language.
    """

    def __init__(self, id, cpvs):
        self.id = id
        self.cpvs = cpvs
        self.lang_entities = {}

    def add_language_entity(self, language_key, title, description=""):
        entity = TenderLanguageEntity(title, description)
        self.lang_entities[language_key] = entity

    def get_title(self, language):
        return self.lang_entities[language].title

    def get_description(self, language):
        return self.lang_entities[language].description

    def get_dict(self):
        contract = {"id": self.id, "cpvs": self.cpvs}
        lang_list = []
        for k, v in self.lang_entities.items():
            lang_entry = {"title": v.title, "description": v.description}
            lang_list.append(lang_entry)
        contract["text"] = lang_list

        return contract
