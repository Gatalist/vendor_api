from flask import jsonify
from app.core.extensions import cache
from app.mti_api.parser import ParserMTI


parser = ParserMTI()


class DatabaseCached:
    def __init__(self):
        self.cached_time = 60 * 60 * 12 # in seconds

    def get_main_categories(self) -> list:
        name_cache = 'main_categories'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные")
            return cached_data
        else:
            print(f"Данные записаны в кэш")
            categories = parser.get_all_categories()
            data_cache = [cat for cat in categories if cat.get('parentID') == 0]
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_all_categories(self) -> list:
        name_cache = 'all_categories'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные")
            return cached_data
        else:
            print(f"Данные записаны в кэш")
            data_cache = parser.get_all_categories()
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_products_category(self, category_id: int) -> dict:
        name_cache = f'products_list_{category_id}'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные для категории {category_id}")
            return cached_data
        else:
            print(f"Данные записаны в кэш")
            data_cache = parser.get_products_for_category(cat_id=category_id)
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            return data_cache

    def get_product_info(self, category_id: int, product_id: int) -> dict:
        name_cache = f'products_list_{category_id}'
        cached_data = cache.get(name_cache)
        if cached_data is not None:
            print(f"Получены закэшированные данные для категории {category_id}")
            data_cache_products_list = cached_data["products_list"]
            product_info = [product for product in data_cache_products_list if product.get('id') == int(product_id)]
            if product_info:
                return product_info[0]
            return {}
        else:
            print(f"Данные записаны в кэш")
            data_cache = parser.get_products_for_category(cat_id=category_id)
            cache.set(name_cache, data_cache, timeout=self.cached_time)
            data_cache_products_list = data_cache["products_list"]
            product_info = [product for product in data_cache_products_list if product.get('id') == int(product_id)]

            if product_info:
                return product_info[0]
            return {}
