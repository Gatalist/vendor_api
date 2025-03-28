import xml.etree.ElementTree as ET
from collections import defaultdict

import requests


class BaseParserMTI:
    def __init__(self):
        self.base_url = 'https://products.mti.ua/api/?action='  # =loadContent&key=Sqceh4xB9PvL'
        self.xml_root = None
        self._key = "Sqceh4xB9PvL"
        self.key = f"&key={self._key}"

    def get_data_from_url(self, url):
        print("url:", url)
        response_data = requests.get(url)
        self.xml_root = ET.fromstring(response_data.content)


class ParserProductList(BaseParserMTI):
    def __init__(self):
        super().__init__()
        self._cat_id = None
        self.cat_id = None
        self.action = "loadContent"
        self.products_count = 0
        self.products_list = []
        self.categories_list = []
        self.params_list = []
        self.params = {}
        self.category_name = ""
        self.url = None

    def generate_data(self, cat_id):
        self._cat_id = cat_id
        self.cat_id = f"&cat_id={cat_id}"
        self.url = self.base_url + self.action + self.key + self.cat_id

    def get_products_count(self):
        self.products_count = self.xml_root.find("products_count").text

    def get_categories_list(self):
        for category in self.xml_root.find("categorieslist").findall("category"):
            self.categories_list.append({
                "id": int(category.get("id")) if category.get("id") else None,
                "parentID": int(category.get("parentID")) if category.get("parentID") else None,
                "name": category.text
            })

    def get_params_list(self):
        for param in self.xml_root.find("paramslist").findall("param"):
            self.params_list.append({
                "type": param.get("type"),
                "code": param.get("code"),
                "name": param.get("name"),
                "in_filter": param.get("in_filter"),
                "multiple": param.get("multiple"),
                "sort": param.get("sort"),
            })
            self.params[param.get("code")] = param.get("name")

    def get_products_list(self):
        for product in self.xml_root.find("productslist").findall("product"):
            card = {
                "id": int(product.get("id")) if product.get("id") else None,
                "cat_id": int(product.get("cat_id")) if product.get("cat_id") else None,
                "photos": [],
                "attributes": [],
            }
            for param in product.findall("param"):
                if param.get("code") == "more_photo":
                    card["photos"].append({param.get('id'): param.text})
                elif param.get("code") == "detail_picture":
                    card["detail_picture"] = param.text
                elif param.get("code") == "name":
                    card["name"] = param.text
                else:
                    card["attributes"].append({
                        "id": param.get('id'),
                        "code_name": param.get("code"),
                        "code_value": self.params.get(param.get("code")),
                        "value": param.text,
                    })
            self.products_list.append(card)

    def get_category_name(self):
        if self.categories_list:
            self.category_name = self.categories_list[-1]["name"]

    def get_all_data(self, cat_id):
        self.generate_data(cat_id)
        self.get_data_from_url(self.url)
        self.get_products_count()
        self.get_categories_list()
        self.get_category_name()
        self.get_params_list()
        self.get_products_list()

        return {
            "products_count": self.products_count,
            "categories_list": self.categories_list,
            # "params_list": self.params_list,
            # "params": self.params,
            "products_list": self.products_list,
            "category_name": self.category_name,
        }


class ParserStructureCategory(BaseParserMTI):
    def __init__(self):
        super().__init__()
        self.action = "getCatalog"
        self.url = self.base_url + self.action + self.key
        self.tree = defaultdict(list)
        self.categories = []

    def get_categories(self):
        self.get_data_from_url(self.url)
        categories_list = self.xml_root.find("categorieslist")
        for category in categories_list.findall("category"):
            cat_id = int(category.attrib["id"]) if category.attrib.get("id") else None
            parent_id = int(category.attrib["parentID"]) if category.attrib.get("parentID") else None
            name = category.text
            self.categories.append({"id": cat_id, "name": name, "parentID": parent_id, })
