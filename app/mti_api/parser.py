import requests
import xml.etree.ElementTree as ET


class Parser:
    def __init__(self, url):
        self.url = url
        self.xml_root = None
        self.products_count = 0
        self.products_list = []
        self.categories_list = []
        self.params_list = []
        self.params = {}
        self.category_name = ""

    def get_data_from_url(self):
        response_data = requests.get(self.url)
        self.xml_root = ET.fromstring(response_data.content)

    def get_products_count(self):
        self.products_count = self.xml_root.find("products_count").text

    def get_categories_list(self):
        for category in self.xml_root.find("categorieslist").findall("category"):
            self.categories_list.append({
                "id": category.get("id"),
                "parentID": category.get("parentID"),
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
                "id": product.get("id"),
                "cat_id": product.get("cat_id"),
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

    def get_all_data(self):
        self.get_data_from_url()
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
