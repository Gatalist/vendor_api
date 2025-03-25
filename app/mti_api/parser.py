# import requests
# import xml.etree.ElementTree as ET
#
# url = "https://products.mti.ua/api/?action=loadContent&key=Sqceh4xB9PvL&cat_id=216"
# response = requests.get(url)
# root = ET.fromstring(response.content)
#
#
# products_count = root.find("products_count").text
# memory_used = root.find("memory_used").text
#
#
#
# print(f"Количество товаров: {products_count}")
# print(f"Использовано памяти: {memory_used} MB")
#
# categories = []
# for category in root.find("categorieslist").findall("category"):
#     categories.append({
#         "id": category.get("id"),
#         "parentID": category.get("parentID"),
#         "name": category.text
#     })
#
# print(categories)
#
#
# params = []
# for param in root.find("paramslist").findall("param"):
#     params.append({
#         "type": param.get("type"),
#         "code": param.get("code"),
#         "name": param.get("name"),
#         "in_filter": param.get("in_filter"),
#         "multiple": param.get("multiple"),
#         "sort": param.get("sort"),#     })
#
# print(params)
