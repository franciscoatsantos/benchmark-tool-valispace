import json
from typing import List, Dict
from api.config import Config


class Importer:

    @classmethod
    def import_collection(cls, data: Dict, api_source: str = "swagger",
                          filters: List = ["get", "post", "put", "delete"]):
        collection = {}
        requests = []
        if api_source in Config.API_IMPORT_FORMATS:
            collection["name"] = data["info"]["title"]
            collection["base_url"] = f'{data["host"]}{data["basePath"]}'

        schemas = {key: schema for key, schema in data["definitions"].items()}

        if collection and "paths" in data.keys():
            requests = cls.parse_requests(data["paths"], filters, schemas)

        return {"collection": collection, "requests": requests}

    @staticmethod
    def parse_requests(requests: Dict, filters: List, schemas: Dict):
        parsed = []
        for key, content in requests.items():
            for k in content.keys():
                if k in filters:
                    parameters = content[k].get("parameters") or []
                    schema_list = []
                    for parameter in parameters:
                        ref = parameter["schema"]["$ref"].split("/")[-1]
                        schema_list.append(ref)
                    request = {
                        "name": content[k]["tags"][0],
                        "url": key,
                        "method": k.upper(),
                        "parameters": [schemas[ref] for ref in schema_list]
                    }

                    parsed.append(request)
        return parsed


class Runner:
    def __init__(self):
        pass
