from flask import jsonify
from app.core.extensions import cache
from app.mti_api.parser import ParserStructureCategory, ParserProductList


structure_category = ParserStructureCategory()
category_indo = ParserProductList()


class DatabaseCached:
    def __init__(self):
        self.cached_time = 60 * 60 * 12 # in seconds

    def get_main_categories(self):
        name_cache = 'main_categories'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные")
            return cached_data
        else:
            print(f"Данные записаны в кэш")
            structure_category.get_categories()
            data_cache = [cat for cat in structure_category.categories if cat.get('parentID') == 0]
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_all_categories(self):
        name_cache = 'all_categories'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные")
            return cached_data
        else:
            print(f"Данные записаны в кэш")
            structure_category.get_categories()
            data_cache = structure_category.categories
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_products_category(self, category_id):
        name_cache = f'products_list_{category_id}'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные для категории {category_id}")
            return cached_data
        else:
            data_cache = category_indo.get_all_data(category_id)
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_product_info(self, category_id, product_id):
        name_cache = f'products_list_{category_id}'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные для категории {category_id}")
            product_info = [product for product in cached_data.get("products_list") if product.get('id') == int(product_id)]
            if product_info:
                return product_info[0]
            return {}
        else:
            data_cache = category_indo.get_all_data(category_id)
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            product_info = [product for product in data_cache.get("products_list") if product.get('id') == int(product_id)]
            if product_info:
                return product_info[0]
            return {}
