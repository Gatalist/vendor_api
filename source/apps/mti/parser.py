import xml.etree.ElementTree as ET
import time
import requests


class ParserMTI:
    def __init__(self):
        self.base_url = 'https://products.mti.ua/api/?action='
        self.xml_root = None
        self.key = f"&key=Sqceh4xB9PvL"
        self.action_product_list = "loadContent"
        self.action_category_list = "getCatalog"
        self.params = {}

    def get_data_from_url(self, cat_id: int = None):
        if cat_id is None:
            url = self.base_url + self.action_category_list + self.key
        else:
            url = self.base_url + self.action_product_list + self.key + f"&cat_id={cat_id}"

        response_data = requests.get(url)
        self.xml_root = ET.fromstring(response_data.content)

    def get_products_count(self):
        return self.xml_root.find("products_count").text

    def get_products_categories(self, last_name: bool = False) -> list:
        categories = []
        for category in self.xml_root.find("categorieslist").findall("category"):
            categories.append({
                "id": int(category.get("id")) if category.get("id") else None,
                "parentID": int(category.get("parentID")) if category.get("parentID") else None,
                "name": category.text
            })
        if last_name:
            if len(categories) == 1:
                last_cat = categories[0]["name"]

            elif len(categories) > 1:
                last_cat = categories[-1]["name"]
            else:
                last_cat = ""
            return last_cat
        else:
            return categories

    def get_params_list(self) -> dict:
        params = {}
        for param in self.xml_root.find("paramslist").findall("param"):
            params[param.get("code")] = param.get("name")
        return params

    def get_products_list(self) -> list:
        params = self.get_params_list()
        products_list = []
        for product in self.xml_root.find("productslist").findall("product"):
            product_id = int(product.get("id")) if product.get("id") else ''
            cat_id = int(product.get("cat_id")) if product.get("cat_id") else ''
            card = {
                "id": product_id,
                "cat_id": cat_id,
                "photos": [],
                "attributes": [],
            }
            for param in product.findall("param"):
                if param.get("code") == "more_photo" and param.text:
                    card["photos"].append({param.get('id'): param.text})
                elif param.get("code") == "detail_picture" and param.text:
                    card["detail_picture"] = param.text
                elif param.get("code") == "name" and param.text:
                    card["name"] = param.text
                else:
                    if param.text:
                        card["attributes"].append({
                            "id": param.get("id") if param.get("id") else f"{time.time()}",
                            "code_name": param.get("code"),
                            "code_value": params.get(param.get("code")),
                            "value": param.text,
                        })

            products_list.append(card)
        return products_list

    def get_products_for_category(self, cat_id: int) -> dict:
        self.get_data_from_url(cat_id)

        return {
            "products_count": self.get_products_count(),
            "products_list": self.get_products_list(),
            "category_name": self.get_products_categories(last_name=True),
        }

    def get_all_categories(self) -> list:
        self.get_data_from_url()
        categories = []
        categories_list = self.xml_root.find("categorieslist")
        for category in categories_list.findall("category"):
            cat_id = int(category.attrib["id"]) if category.attrib.get("id") else None
            parent_id = int(category.attrib["parentID"]) if category.attrib.get("parentID") else None
            name = category.text
            categories.append({"id": cat_id, "name": name, "parentID": parent_id, })
        return categories