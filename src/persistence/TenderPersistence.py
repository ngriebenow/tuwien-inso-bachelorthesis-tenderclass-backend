import json

from src.entity.Tender import Tender


class TenderPersistence:

    def save(self, tenders, path):
        with open("data/" + path, 'w', encoding='utf8') as json_file:
            json.dump(list(map(lambda x: x.get_dict(), tenders)), json_file, ensure_ascii=False)

    def load(self, path):
        with open("data/" + path, 'r', encoding='utf8') as json_file:
            tender_dicts = json.load(json_file)
        tenders = list(map(lambda x: Tender.from_json_dict(x), tender_dicts))
        return tenders
