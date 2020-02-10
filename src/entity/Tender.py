from typing import List

from src.entity.TenderLanguageEntity import TenderLanguageEntity


class Tender:
    """
    This class serves as entity for one tender. It holds the id, the CPV codes and a number of language entities,
    where each of which is a collection of title and description in a certain language.
    """

    @classmethod
    def from_json_dict(cls, serialized_dict):
        id = serialized_dict["id"]
        cpvs = serialized_dict["cpvs"]
        lang_entities = {}
        for e in serialized_dict["languageentities"]:
            lang_entry = TenderLanguageEntity(e["title"], e["description"])
            lang_entities[e["language"]] = lang_entry
        return cls(id, cpvs, lang_entities)

    def __init__(self, id: str, cpvs: List[str], lang_entities=None):
        self.id = id
        self.cpvs = cpvs
        if lang_entities is None:
            lang_entities = {}
        self.lang_entities = lang_entities

    def add_language_entity(self, language_key, title, description="", link=""):
        entity = TenderLanguageEntity(title, description, link)
        self.lang_entities[language_key] = entity

    def get_title(self, language):
        return self.lang_entities[language].title

    def get_description(self, language):
        return self.lang_entities[language].description

    def get_dict(self):
        contract = {"id": self.id, "cpvs": list(self.cpvs)}
        lang_list = []
        for k, v in self.lang_entities.items():
            lang_entry = {"language": k, "title": v.title, "description": v.description, "link": v.link}
            lang_list.append(lang_entry)
        contract["languageentities"] = lang_list

        return contract
